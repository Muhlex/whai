import { writable, type Updater, type Subscriber } from "svelte/store";

export default class Reactive {
	#store = writable(this);

	// Expose store's methods on our class instances:
	subscribe(run: Subscriber<this>, invalidate?: () => void) {
		return this.#store.subscribe(run, invalidate);
	}
	set(value: this) {
		return this.#store.set(value);
	}
	update(updater: Updater<this>) {
		return this.#store.update(updater);
	}

	// Notify the underlying svelte store that data has been changed.
	// Needs to be called every time we change (public) fields.
	notify() {
		this.#store.set(this);
	}
}
