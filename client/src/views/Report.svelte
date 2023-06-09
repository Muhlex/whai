<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { marked } from 'marked';
	import DOMPurify from 'dompurify';
	import { buildURL } from '../api';
	import { user, reports } from "../stores";
	import { recordAudio, shuffleArray, type Recorder } from '../util';
  import type { Entry } from '../models/Report';

	import Header from "../lib/Header.svelte";
	import Icon from "../lib/Icon.svelte";
	import Button from "../lib/Button.svelte";
	import NotFound from './NotFound.svelte';
  import ReportPrint from '../lib/ReportPrint.svelte';

	export let params: { id?: string, edit?: boolean } = {};

	$: report = $reports.get(Number(params.id));
	$: edit = Boolean(params.edit);

	const onUpdateDate = (event: Event) => {
		const target = event.target as HTMLInputElement;
		$report.date = target.valueAsDate;
	};

	let recorders: { problem: Recorder, solution: Recorder } = { problem: null, solution: null };

	const record = async (recorderID: keyof typeof recorders) => {
		let recorder = recorders[recorderID] as Recorder;
		if (!recorder) {
			recorder = await recordAudio();
			recorders[recorderID] = recorder;
			recorder.start();
		} else {
			let entry: Entry = null;
			try {
				recorder = recorders[recorderID];
				const { blob } = await recorder.stop();
				recorders[recorderID] = null;

				entry = { text: "", status: "pending" };
				const entries = $report[recorderID];
				entries.push(entry);
				$report = $report;

				const formData = new FormData();
				formData.append("file", blob);
				const res = await fetch(buildURL("/transcribe-file/"), { method: "POST", body: formData });

				if (!res.ok) {
					throw new Error(`${res.status} (${res.statusText})`);
				}

				const { transcription } = await res.json();
				entry.status = undefined;
				entry.text = transcription;
				$report = $report;
			} catch (error) {
				console.error(error);
				if (entry) {
					const index = $report[recorderID].indexOf(entry);
					if (index > -1) $report[recorderID].splice(index, 1);
					$report = $report;
				}
			} finally {
				recorders[recorderID] = null;
			}
		}
	};

	const translate = async (entry: Entry) => {
		entry.status = "pending";
		$report = $report;
		try {
			const url = buildURL("/translate/");
			if (emojiMode) url.searchParams.append("emoji", "true");
			const res = await fetch(url, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ text: entry.text, language: $user.language }),
			});
			handleTranslatedResponse(res, entry);
		} catch (error) {
			console.error(error);
			entry.status = "error";
			$report = $report;
		}
	};

	const handleTranslatedResponse = async (res: Response, entry: Entry) => {
		const { chat_gpt_translation: gpt, azure_translation: azure, score } = await res.json();
		console.log({ _input: entry.text, gpt, azure, score });
		if (emojiMode) {
			entry.text = gpt;
			entry.status = "success";
		} else {
			if (score > 50) {
				entry.text = azure;
				entry.status = "success";
			} else if (score > 20) {
				entry.text = gpt;
				entry.status = "success";
			} else {
				entry.status = "error";
			}
		}
		$report = $report;
	};

	$: summaryAvailable = $user.language.split("-")[0] === "en"
		&& $report.solution.reduce((charCount, { text }) => charCount + text.length, 0) > 250;
	let gettingSummary = false;

	const updateSummary = async () => {
		gettingSummary = true;
		try {
			const res = await fetch(buildURL("/summarize/"), {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ text: $report.solution.map(p => p.text).join("; "), length: "medium" }),
			});
			if (!res.ok) {
				console.error(new Error(`${res.status} (${res.statusText})`));
				return;
			}
			const markdown = await res.json();
			console.log("Summary:\n\n", markdown);
			$report.summary = DOMPurify.sanitize(marked.parse(markdown));
		} catch (error) {
			console.error(error);
		} finally {
			gettingSummary = false;
		}
	}

	let mounted = false;
	onMount(() => {
		mounted = true;
	});

	$: if (mounted && edit === false) {
		$report?.trim();
	}
	onDestroy(() => {
		$report?.trim();
	});

	let emojiModeCurrentIndex = 0;
	let emojiMode = false;
	const emojis = shuffleArray(['😀','😃','😄','😁','😆','😅','🤣','😂','🙂','🙃','😉','😊','😇'])
		.slice(0, 8)
		.join("");
	const onKeyPress = (event: KeyboardEvent) => {
		const passkey = "EMOJI!";
		const letter = event.key;
		if (letter === passkey[emojiModeCurrentIndex]) {
			emojiModeCurrentIndex++;
			if (emojiModeCurrentIndex === passkey.length) emojiMode = true;
		} else {
			emojiModeCurrentIndex = 0;
		}
	}

	onMount(() => document.addEventListener("keypress", onKeyPress));
	onDestroy(() => document.removeEventListener("keypress", onKeyPress));

	let printComponent;
	const generatePDF = async () => {
		const html = printComponent.getHTML();
		const res = await fetch(buildURL("/pdf/"), {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ report: html }),
		});
		if (!res.ok) {
			console.error(new Error(`${res.status} (${res.statusText})`));
			return;
		}
		const blob = await res.blob();
		return blob;
	};

	const downloadPDF = async () => {
		try {
			if (!$report.file?.url) {
				const blob = await generatePDF();
				report.setFile(blob);
			}
			const a = document.createElement('a');
			a.download = `${$report.title}.pdf`;
			a.href = $report.file.url;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
		} catch (error) {
			console.error(error);
		}
	};
</script>

{#if emojiMode}
	{emojis}
{/if}
{#if report}
	<ReportPrint bind:this={printComponent} {report} hide />
	<div class="report">
		<Header>
			<h1>
				{#if edit}
					<span class="title" contenteditable bind:innerText={$report.title} />
				{:else}
					<span class="title">{$report.title}</span>
				{/if}
				<span class="id">#{$report.id}</span>
			</h1>
			<svelte:fragment slot="buttons">
				{#if edit}
					<Button
						color="primary"
						element="a"
						href="#/report/{$report.id}"
						icon="check"
					>
						Done
					</Button>
				{:else}
					<Button
						color="primary"
						icon="file-download"
						on:click={downloadPDF}
					>
						Download
					</Button>
					<Button
						color="attention"
						element="a"
						href="#/report/{$report.id}/edit"
						icon="edit"
					>
						Edit
					</Button>
				{/if}
			</svelte:fragment>
		</Header>
		<div class="meta">
			<div class="date-group">
				<Icon name="date" />
				{#if edit}
					<input
						type="date"
						class="date"
						required
						value={$report.date.toISOString().split("T")[0]}
						on:input={onUpdateDate}
					>
				{:else}
					<span class="date">{$report.date.toLocaleDateString(undefined, { dateStyle: 'full' })}</span>
				{/if}
			</div>
			{#if $report.location || edit}
				<div class="location-group">
					<Icon name="location" />
					{#if edit}
						<span class="location" contenteditable bind:innerText={$report.location} />
					{:else}
						<span class="location">{$report.location}</span>
					{/if}
				</div>
			{/if}
			<div class="author-group">
				<Icon name="user" />
				by <i>{$user.name}</i>
			</div>
		</div>

		<div class="body">
			<div class="problem">
				<h3>Description of problem / maintenance / inspection</h3>
				{#if $report.problem.length}
					{#each $report.problem as entry}
						{#if edit}
							<div class="edit-row">
								<p contenteditable bind:innerText={entry.text} class={entry.status} />
								<Button
									variant="text"
									color="attention"
									size="0.875em"
									icon="translate"
									on:click={() => translate(entry)}
								/>
							</div>
						{:else}
							<p>{entry.text}</p>
						{/if}
					{/each}
				{:else}
					<p><i>No description given.</i></p>
				{/if}
				{#if edit}
					<div class="buttons">
						<Button
							block shape="pill" variant="outline" icon="pencil"
							on:click={() => {
								$report.problem.push({ text: "" });
								$report.problem = $report.problem;
							}}
						>
							Write
						</Button>
						<Button
							block shape="pill" variant="outline" icon={recorders.problem ? "mic-off" : "mic"}
							on:click={() => record("problem")}
						>
							{recorders.problem ? 'Stop' : 'Record'}
						</Button>
						<Button style="visibility: hidden" variant="text" icon="translate" />
					</div>
				{/if}
			</div>

			<div class="solution">
				<h3>Reason and solution of the problem / accomplished work</h3>
				{#if $report.solution.length}
					{#each $report.solution as entry}
						{#if edit}
							<div class="edit-row">
								<p contenteditable bind:innerText={entry.text} class={entry.status} />
								<Button
									variant="text"
									color="attention"
									size="0.875em"
									icon="translate"
									on:click={() => translate(entry)}
								/>
							</div>
						{:else}
							<p>{entry.text}</p>
						{/if}
					{/each}
				{:else}
					<p><i>No possible reason or solution given.</i></p>
				{/if}
				{#if edit}
					<div class="buttons">
						<Button
							block shape="pill" variant="outline" icon="pencil"
							on:click={() => {
								$report.solution.push({ text: "" });
								$report.solution = $report.solution;
							}}
						>
							Write
						</Button>
						<Button
							block shape="pill" variant="outline" icon={recorders.solution ? "mic-off" : "mic"}
							on:click={() => record("solution")}
						>
							{recorders.solution ? 'Stop' : 'Record'}
						</Button>
						<Button style="visibility: hidden" variant="text" icon="translate" />
					</div>
				{/if}
			</div>
		</div>

		{#if $report.summary || summaryAvailable}
			<div class="summary">
				<h3>Summary</h3>
				{#if $report.summary}
					<div class="summary-text">
						{@html $report.summary}
					</div>
				{/if}
				{#if summaryAvailable}
					<Button
						variant={edit ? "fill" : "text"}
						icon="list"
						size="0.875em"
						disabled={gettingSummary}
						on:click={updateSummary}
					>
						{$report.summary ? "Update" : "Generate"} Summary
					</Button>
				{/if}
			</div>
		{/if}
	</div>
{:else}
	<NotFound />
{/if}

<style>
	[contenteditable] {
		background-color: hsl(var(--c-primary-hsl), 0.5);
		padding: 0 0.25em;
		min-width: 5em;
	}
	span[contenteditable] {
		display: inline-block;
	}
	span[contenteditable]::before {
		content: "\200b";
	}

	.report {
		display: flex;
		flex-direction: column;
		gap: 1em;
	}

	.id {
		opacity: 0.5;
		font-weight: 400;
	}

	.date-group {
		font-weight: bold;
	}

	.body {
		margin-top: 4em;

		display: flex;
		flex-wrap: wrap;
		gap: 4em;
	}

	.body .problem {
		flex-basis: 200px;
		flex-grow: 1;
	}
	.body .solution {
		flex-basis: 400px;
		flex-grow: 1;
	}

	.body > * {
		display: flex;
		flex-direction: column;
		gap: 1em;
	}

	.summary {
		margin-top: 4em;
	}

	p {
		margin: 0;
	}

	.edit-row {
		display: flex;
		align-items: center;
		gap: 0.5em;
	}
	.edit-row p {
		flex-grow: 1;
	}

	input[type=date] {
		appearance: none;
		color: inherit;
		background-color: hsl(var(--c-primary-hsl), 0.5);
		border: none;
		font: inherit;
	}

	.buttons {
		display: flex;
		gap: 0.5em;
	}

	.pending {
		animation: pulse 2000ms ease infinite;
	}
	.success {
		background-color: hsl(185, var(--c-primary-s), var(--c-primary-l), 0.4);
	}
	.error {
		background-color: hsl(var(--c-attention-hsl), 0.4);
	}

	@keyframes pulse {
		0%   { opacity: 0.4; }
		50%  { opacity: 0.9; }
		100% { opacity: 0.4; }
	}
</style>
