<script lang="ts">
	import Router, { location, replace } from 'svelte-spa-router'
	import routes from "./routes";
  import { introDone } from './stores';

	$: {
		void $location;
		if (!$introDone) replace("#/intro");
	}
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
		min-width: 280px;
		max-width: 1140px;
		margin: 0 auto;
		padding: 1em;
	}
</style>
