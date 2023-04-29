<script lang="ts">
	import Button from "./Button.svelte";
</script>

<div class="header">
	<slot />
	<div class="buttons">
		<slot name="buttons" />
		<Button icon="home-line" color="shade" element="a" href="#/" />
	</div>
</div>

<style>
	.header {
		display: flex;
		gap: 1em;
		align-items: flex-start;
		flex-wrap: wrap-reverse;
	}
	.buttons {
		margin-left: auto;

		display: flex;
		gap: 0.5em;
	}
</style>
