<script lang="ts">
	import { user } from "../stores";
  import { Report } from "../models/Report";

	export let report: Report;
	export let hide = false;

	let reportEl: HTMLElement = null;
	export const getHTML = () => {
		return `\
			<html>\
				<head>
					<meta charset="utf-8">
					<style>
						@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,700&display=block');
						body {
							font-family: 'IBM Plex Sans';
						}
					</style>
				</head>\
				<body>\
					${reportEl.outerHTML}\
				</body>\
			</html>`;
	};
</script>

<div class="report" style:display={hide ? "none" : undefined}>
	<article bind:this={reportEl}>
		<h1>
			<span class="title">{$report.title}</span>
			<small class="id">#{$report.id}</small>
		</h1>

		<section class="meta">
			<p class="date">
				<span class="icon">
					📅
				</span>
				<span class="text">
					{$report.date.toLocaleDateString(undefined, { dateStyle: 'full' })}
				</span>
			</p>
			{#if $report.location}
				<p class="location">
					<span class="icon">
						📍
					</span>
					<span class="text">
						{$report.location}
					</span>
				</p>
				{/if}
			<p class="author">
				<span class="icon">
					👤
				</span>
				<span class="text">
					{$user.name}
				</span>
			</p>
		</section>

		<hr>

		<section class="body">
			<div class="problem">
				<h3>Description of problem / maintenance / inspection</h3>
				{#if $report.problem.length}
					{#each $report.problem as entry}
						<p>{entry.text}</p>
					{/each}
				{:else}
					<p><i>No description given.</i></p>
				{/if}
			</div>

			<div class="solution">
				<h3>Reason and solution of the problem / accomplished work</h3>
				{#if $report.solution.length}
					{#each $report.solution as entry}
						<p>{entry.text}</p>
					{/each}
				{:else}
					<p><i>No possible reason or solution given.</i></p>
				{/if}
			</div>
		</section>

		{#if $report.summary}
			<div class="summary">
				<h3>Summary</h3>
				<div class="summary-text">
					{@html $report.summary}
				</div>
			</div>
		{/if}
	</article>
</div>
