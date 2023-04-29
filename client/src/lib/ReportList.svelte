<script lang="ts">
	import { reports } from "../stores";
  import Button from "./Button.svelte";
</script>

<ul>
	{#each [...$reports.values()] as report}
		<li>
			<Button element="a" variant="reset" href={`#/report/${report.id}`}>
				<div class="date">
					{ report.date.toLocaleDateString(undefined, { dateStyle: 'short' }) }
				</div>
				<div class="title">
					{ report.title }
				</div>
			</Button>
		</li>
	{/each}
</ul>

<style>
ul {
	list-style: none;
	padding: 0;
	margin: 0;
	border-radius: 4px;
	overflow: hidden;
}

li {
	display: flex;
	gap: 1em;
}

li:not(:last-child) {
	border-bottom: 1px solid hsl(var(--c-fore-hsl), 0.3);
}
li:nth-child(odd) {
	background-color: hsl(var(--c-fore-hsl), 0.1);
}
li:nth-child(even) {
	background-color: hsl(var(--c-fore-hsl), 0.05);
}

li :global(a) {
	flex-grow: 1;
	padding: 0.75em 1em;

	display: flex;
	gap: 0.5em;

	transition: background-color 200ms;
}
li :global(a):hover {
	background-color: hsl(var(--c-fore-hsl), 0.1);
}

.date {
	font-weight: 500;
}
</style>
