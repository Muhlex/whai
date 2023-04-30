<script lang="ts">
import { user, languages } from "../stores";
import Header from "../lib/Header.svelte";
</script>

<Header>
	<h1>Settings</h1>
</Header>

<div class="settings">
	<div class="setting">
		<h2>Your Name</h2>
		<input type="text" bind:value={$user.name}>
	</div>
	<div class="setting">
		<h2>Languages</h2>
		<h3>Target Language</h3>
		<select bind:value={$user.language}>
			{#each Object.entries(languages) as [lc, name]}
				<option value={lc}>
					{name}
				</option>
			{/each}
		</select>
	</div>
</div>

<style>
	.settings {
		display: flex;
		flex-direction: column;
		gap: 4em;
		margin-top: 4em;
	}

	.setting {
		display: flex;
		flex-direction: column;
	}
</style>
