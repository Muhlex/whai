<script lang="ts">
	import Button from "../lib/Button.svelte";
	import Header from "../lib/Header.svelte";
	import ReportList from "../lib/ReportList.svelte";
	import { createReport } from "../stores";
	import { push } from "svelte-spa-router";

	const addReport = () => {
		const { id } = createReport({ problem: [""], solution: [""] });
		push(`#/report/${id}/edit`);
	};
</script>

<div class="home">
	<div class="content">
		<Header hideHome>
			<h1>DengL <small>by whAI</small></h1>
			<svelte:fragment slot="buttons">
				<Button
					color="primary"
					element="a"
					href="#/settings"
					icon="settings"
				>
					Settings
				</Button>
			</svelte:fragment>
		</Header>


		<h2>Reports</h2>
		<ReportList />
	</div>


	<div class="new">
		<Button shape="pill" block on:click={addReport}>New Report</Button>
	</div>
</div>

<style>
	.home {
		flex-grow: 1;

		display: flex;
		flex-direction: column;
		gap: 1em;
	}

	.content {
		flex-basis: 0;
		flex-grow: 1;
		overflow-y: auto;
	}

	.new {
		flex-shrink: 0;

		display: flex;
		gap: 0.5em;
		margin-top: auto;
	}

	small {
		opacity: 0.75;
	}
</style>
