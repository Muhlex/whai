<script lang="ts">
	import Button from "./Button.svelte";

	export let hideHome = false;
</script>

<div class="header">
	<slot />
	<div class="buttons">
		<slot name="buttons" />
		{#if !hideHome}
			<Button icon="home-line" color="shade" element="a" href="#/" />
		{/if}
	</div>
</div>

<style>
	.header {
		display: flex;
		gap: 1em;
		align-items: flex-start;
		flex-wrap: wrap-reverse;
	}

	.header :global(h1) {
		margin: 0;
	}

	.buttons {
		margin-left: auto;

		display: flex;
		gap: 0.5em;
	}
</style>
