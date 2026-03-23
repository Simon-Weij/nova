<script lang="ts">
	import { password } from '$lib/store';
	import { get } from 'svelte/store';

	let wakeWords = $state([{ id: crypto.randomUUID(), value: '' }]);

	function addWakeWord() {
		wakeWords = [...wakeWords, { id: crypto.randomUUID(), value: '' }];
	}

	function removeWakeWord(id: string) {
		wakeWords = wakeWords.filter((w) => w.id !== id);
	}

	async function saveWakeWord() {
		const requestHeaders: Record<string, string> = {
			'x-api-key': get(password)
		};
		await fetch('/api/settings/upload', {
			method: 'POST',
			headers: requestHeaders,
			body: JSON.stringify({
				wakeWords
			})
		});
	}
</script>

<div class="flex flex-col justify-center rounded-lg bg-white p-4">
	<h1 class="border-b text-center text-2xl font-bold">Wake words</h1>

	{#each wakeWords as word (word.id)}
		<div class="mt-2 flex gap-2">
			<input
				type="text"
				bind:value={word.value}
				placeholder="e.g. Hello Nova"
				class="w-full rounded border border-gray-300 p-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
			/>
			{#if wakeWords.length > 1}
				<button
					onclick={() => removeWakeWord(word.id)}
					class="cursor-pointer rounded bg-red-100 px-3 text-red-600 hover:bg-red-200"
				>
					✕
				</button>
			{/if}
		</div>
	{/each}

	<button
		onclick={addWakeWord}
		class="mt-3 cursor-pointer rounded border border-dashed border-blue-400 py-1 text-blue-500 hover:bg-blue-50"
	>
		+ Add wake word
	</button>
	<button
		onclick={saveWakeWord}
		class="text-white-500 mt-3 cursor-pointer rounded border border-blue-400 bg-blue-400 py-1 hover:bg-blue-600"
	>
		Save
	</button>
</div>
