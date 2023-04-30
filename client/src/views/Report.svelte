<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { buildURL } from '../api';
	import { user, reports } from "../stores";
	import { recordAudio, type Recorder } from '../util';
  import type { Entry } from '../models/Report';

	import Header from "../lib/Header.svelte";
	import Icon from "../lib/Icon.svelte";
	import Button from "../lib/Button.svelte";
	import NotFound from './NotFound.svelte';

	export let params: { id?: string, edit?: boolean } = {};

	$: report = $reports.get(Number(params.id));
	$: edit = Boolean(params.edit);

	let recorders: { problem: Recorder, solution: Recorder } = { problem: null, solution: null };

	const record = async (recorderID: keyof typeof recorders) => {
		let recorder = recorders[recorderID] as Recorder;
		if (!recorder) {
			recorder = await recordAudio();
			recorders[recorderID] = recorder;
			recorder.start();
		} else {
			try {
				recorder = recorders[recorderID];
				const { blob } = await recorder.stop();
				recorders[recorderID] = null;

				const entry = { text: "", status: "pending" } as Entry;
				$report[recorderID].push(entry);
				$report[recorderID] = $report[recorderID];

				const formData = new FormData();
				formData.append("file", blob);
				const url = buildURL("/upload-file/");
				url.searchParams.append("lang_to", $user.language);
				const res = await fetch(url, { method: "POST", body: formData });
				handleTranslatedResponse(res, entry, $report[recorderID], true);
			} finally {
				recorders[recorderID] = null;
			}
		}
	};

	const translate = async (entry: Entry, entries: Entry[]) => {
		entry.status = "pending";
		$report = $report;
		try {
			const res = await fetch(buildURL("/translate/"), {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ text: [entry.text], language: $user.language }),
			});
			handleTranslatedResponse(res, entry, entries);
		} catch (error) {
			console.error(error);
			entry.status = "error";
			$report = $report;
		}
	};

	const handleTranslatedResponse = async (res: Response, entry: Entry, entries: Entry[], deleteOnFail = false) => {
		if (!res.ok) {
			console.error(new Error(`${res.status} (${res.statusText})`));
			if (deleteOnFail) {
				const index = entries.indexOf(entry);
				if (index > -1) entries.splice(index, 1);
				$report = $report;
			}
			return;
		}

		const { chat_gpt_translation: gpt, azure_translation: azure, score } = await res.json();
		console.log({ previously: entry.text, gpt, azure, score });
		if (score > 90) {
			entry.text = azure;
			entry.status = "success";
		} else if (score > 20) {
			entry.text = gpt;
			entry.status = "success";
		} else {
			entry.status = "error";
		}
		$report = $report;
	};

	const onUpdateDate = (event: Event) => {
		const target = event.target as HTMLInputElement;
		$report.date = target.valueAsDate;
	};

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
</script>

{#if report}
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
									color="shade"
									size="0.875em"
									icon="translate"
									on:click={() => translate(entry, $report.problem)}
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
									color="shade"
									size="0.875em"
									icon="translate"
									on:click={() => translate(entry, $report.solution)}
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
	</div>
{:else}
	<NotFound />
{/if}

<style>
	[contenteditable] {
		background-color: hsl(var(--c-primary-hsl), 0.5);
		padding: 0 0.25em;
		min-width: 2em;
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
		background-color: hsl(200, var(--c-primary-s), var(--c-primary-l), 0.5);
	}
	.error {
		background-color: hsl(var(--c-attention-hsl), 0.5);
	}

	@keyframes pulse {
		0%   { opacity: 0.4; }
		50%  { opacity: 0.9; }
		100% { opacity: 0.4; }
	}
</style>
