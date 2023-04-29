<script lang="ts">
	import Icon from "./Icon.svelte";

	export let element = "button";
	export let variant: "fill" | "outline" | "text" | "reset" = "fill";
	export let shape: "default" | "pill" | "ellipse" = "default";
	export let block = false;
	export let color = "primary";
	export let size = "1em";
	export let icon = undefined;
</script>

<svelte:element
	this={element}
	class="button {variant} {shape}"
	class:block
	style:--color-h="var(--c-{color}-h)"
	style:--color-s="var(--c-{color}-s)"
	style:--color-l="var(--c-{color}-l)"
	style:font-size={size}
	{...$$restProps}
	on:click
>
	{#if icon}
		<Icon name={icon} />
	{/if}
	<slot />
</svelte:element>

<style lang="postcss">
	.button {
		--color: hsl(var(--color-h), var(--color-s), var(--color-l));
		--color-shade: transparent;

		appearance: none;
		border: none;
		background: none;
		color: currentColor;
		font: inherit;
		text-align: inherit;
		text-decoration: none;
	}
	.button:not(.reset) {
		display: inline-flex;
		justify-content: center;
		align-items: center;
		gap: 0.25em;

		border-radius: 4px;
		border: 2px solid transparent;
		padding: 0.75em 1em;
		font-weight: 500;
		text-align: center;
		cursor: pointer;

		transition: ease 300ms;
		transition-property: background-color, border-color, color;
	}
	.button:hover {
		--color: hsl(var(--color-h), var(--color-s), calc(var(--color-l) + 10%));
		--color-shade: hsl(var(--color-h), calc(var(--color-s) + 20%), calc(var(--color-l) + 20%), 0.1);
	}

	.button.fill {
		background-color: var(--color);
		color: white;
	}
	.button.outline {
		background-color: var(--color-shade);
		border-color: var(--color);
		color: var(--color);
	}
	.button.text {
		background-color: var(--color-shade);
		color: var(--color);
	}
	.button.outline, .button.text {
		--color: hsl(var(--color-h), var(--color-s), calc(var(--color-l) + 20%));
	}
	.button.outline:hover, .button.text:hover {
		--color: hsl(var(--color-h), var(--color-s), calc(var(--color-l) + 30%));
	}

	.button.pill {
		border-radius: max(1000vw, 1000vh);
	}
	.button.ellipse {
		border-radius: 50%;
		padding: 0.5em;
	}

	.button.block {
		display: block;
		width: 100%;
		flex-grow: 1;
	}
</style>
