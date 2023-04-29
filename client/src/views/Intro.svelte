<script lang="ts">
  import { push } from "svelte-spa-router";
	import Button from "../lib/Button.svelte";
	import { introDone, languages, user } from "../stores";

	let step = 0;

	const finish = () => {
		$introDone = true;
		push("#/");
	}
</script>

<h1>Welcome to DengL!</h1>
{#if step === 0}
	<h2>Please enter your name to have your reports matched to you correctly.</h2>
	<form on:submit|preventDefault={() => step++}>
		<input type="text" required minlength="2" placeholder="John Doe" bind:value={$user.name}>
		<Button type="submit">Continue</Button>
	</form>
	{:else if step === 1}
	<h2>Choose the langauge of your reports.</h2>
	<form on:submit|preventDefault={finish}>
		<select bind:value={$user.languages[0]}>
			{#each Object.entries(languages) as [lc, name]}
			<option value={lc}>
				{name}
			</option>
			{/each}
		</select>
		<h2>Choose an additional language to translate dynamically.</h2>
		<select bind:value={$user.languages[1]}>
			{#each Object.entries(languages) as [lc, name]}
				<option value={lc}>
					{name}
				</option>
			{/each}
		</select>
		<Button type="submit">Let's get started!</Button>
	</form>
{/if}

<style>
	form {
		display: flex;
		flex-direction: column;
		gap: 1em;
	}
</style>
