<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { user, reports } from "../stores";
	import { recordAudio, type Recorder } from '../util';
	import Header from "../lib/Header.svelte";
	import Icon from "../lib/Icon.svelte";
	import Button from "../lib/Button.svelte";

	export let params: { id?: string, edit?: boolean } = {};

	$: report = $reports.get(Number(params.id));
	$: edit = Boolean(params.edit);
	let recorders: { problem: Recorder, solution: Recorder } = { problem: null, solution: null };
	const record = async (recorderID: string) => {
		let recorder = recorders[recorderID] as Recorder;
		if (!recorder) {
			recorder = await recordAudio();
			recorders[recorderID] = recorder;
			recorder.start();
		} else {
			try {
				recorder = recorders[recorderID];
				const { play } = await recorder.stop();
				play();
			} finally {
				recorders[recorderID] = null;
			}
		}
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
		$report.trim();
	}
	onDestroy(() => {
		$report.trim();
	});
</script>

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
				{#each $report.problem as paragraph}
					{#if edit}
						<p contenteditable bind:innerText={paragraph} />
					{:else}
						<p>{paragraph}</p>
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
							$report.problem.push("");
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
				</div>
			{/if}
		</div>

		<div class="solution">
			<h3>Reason and solution of the problem / accomplished work</h3>
			{#if $report.solution.length}
				{#each $report.solution as paragraph}
					{#if edit}
						<p contenteditable bind:innerText={paragraph} />
					{:else}
						<p>{paragraph}</p>
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
							$report.solution.push("");
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
				</div>
			{/if}
		</div>
	</div>
</div>

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

	h1 {
		margin: 0;
	}

	.id {
		opacity: 0.5;
		font-weight: 400;
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

	.date-group {
		font-weight: bold;
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
</style>