<script lang="ts">
	import Router from 'svelte-spa-router'
	import routes from "./routes";
</script>

<main>
	<Router {routes} />
</main>

<style>
	main {
		flex-grow: 1;

		display: flex;
		flex-direction: column;
		width: 100%;
		min-width: 320px;
		max-width: 1140px;
		margin: 0 auto;
		padding: 1em;
	}
</style>
