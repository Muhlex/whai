<script>
	export let name;
	export let size = "1em";
	export let width = size;
	export let height = size;
	export let color = "currentColor";

	$: icon = import(`../assets/icons/${name}.svg?raw`);
</script>
<div class="icon" style:width style:height style:color>
	{#await icon then { default: html }}
		{@html html}
	{/await}
</div>

<style>
	.icon {
		display: inline-block;
		vertical-align: -10%;
	}

	.icon :global(svg) {
		display: block;
	}
</style>
