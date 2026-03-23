<script lang="ts">
	import { goto } from '$app/navigation';
	import { password } from '$lib/store';
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';

	type Model = {
		name: string;
		size: string;
	};

	const popularModels = [
		{ label: 'Llama 3.2 (3B)', value: 'llama3.2:3b' },
		{ label: 'Gemma 3 (1B)', value: 'gemma3:1b' },
		{ label: 'Qwen 2.5 (1.5B)', value: 'qwen2.5:1.5b' },
		{ label: 'TinyLlama (1.1B)', value: 'tinyllama' },
		{ label: 'Custom', value: 'custom' }
	];

	let selectedModel = $state(popularModels[0].value);
	let customModel = $state('');
	let newModel = $state('');

	let isLoading = $state(false);
	let isInstalling = $state(false);
	let deletingModel = $state('');
	let actionError = $state('');

	let models: Model[] = $state([]);

	$effect(() => {
		if (selectedModel === 'custom') {
			newModel = customModel.trim();
			return;
		}

		newModel = selectedModel.trim();
	});

	export async function apiRequest(
		url: string,
		options: RequestInit = {},
		errorMessage = 'Request failed',
		allowedStatuses: number[] = []
	) {
		actionError = '';

		const requestHeaders = {
			'x-api-key': get(password),
			...(options.headers as Record<string, string> | undefined)
		};

		try {
			const response = await fetch(url, {
				...options,
				headers: requestHeaders
			});

			if (!response.ok && !allowedStatuses.includes(response.status)) {
				actionError = `${errorMessage} (${response.status})`;
				return null;
			}

			return response;
		} catch {
			actionError = errorMessage;
			return null;
		}
	}

	async function checkAuth() {
		const res = await apiRequest('/api/auth/check', {}, 'Auth check failed', [401]);
		if (!res) {
			return false;
		}

		if (res.status === 401) {
			await goto('/setup');
			return false;
		}

		return true;
	}

	async function loadModels() {
		isLoading = true;
		const res = await apiRequest('/api/models', {}, 'Could not load models');

		if (res) {
			models = (await res.json()) as Model[];
		}

		isLoading = false;
	}

	async function installNewModel() {
		if (!newModel || isInstalling || deletingModel !== '') {
			return;
		}

		isInstalling = true;
		const response = await apiRequest(
			'/api/models',
			{
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ model_name: newModel })
			},
			'Install failed'
		);

		if (response) {
			if (selectedModel === 'custom') {
				customModel = '';
			}

			await loadModels();
		}

		isInstalling = false;
	}

	async function deleteModel(modelName: string) {
		if (isInstalling || deletingModel !== '') {
			return;
		}

		deletingModel = modelName;
		const response = await apiRequest(
			`/api/models/${encodeURIComponent(modelName)}`,
			{
				method: 'DELETE'
			},
			'Delete failed'
		);

		if (response) {
			await loadModels();
		}

		deletingModel = '';
	}

	onMount(async () => {
		if (await checkAuth()) {
			await loadModels();
		}
	});
</script>

<div class="flex flex-col justify-center rounded-lg bg-white p-4">
	<h1 class="border-b text-center text-2xl font-bold">Model Configuration</h1>

	<p class="mt-3 font-semibold">Installed models</p>
	{#if isLoading}
		<p class="mt-2 text-sm text-gray-600">Loading…</p>
	{:else if models.length === 0}
		<p class="mt-2 text-sm text-gray-600">No models installed yet.</p>
	{:else}
		<ul class="mt-2 flex flex-col gap-2">
			{#each models as model (model.name)}
				<li class="flex items-center justify-between gap-2 rounded border p-2 text-sm">
					<div>
						<p>{model.name}</p>
						<p class="text-xs text-gray-500">{model.size}</p>
					</div>
					<button
						onclick={() => deleteModel(model.name)}
						disabled={isInstalling || deletingModel !== ''}
						class="cursor-pointer rounded bg-red-300 px-4 py-2 text-black"
					>
						{#if deletingModel === model.name}
							Deleting…
						{:else}
							Delete
						{/if}
					</button>
				</li>
			{/each}
		</ul>
	{/if}

	<p class="mt-5 font-semibold">Install new model</p>
	<select
		bind:value={selectedModel}
		class="mt-1 w-full rounded border border-gray-300 p-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
	>
		{#each popularModels as modelOption (modelOption.value)}
			<option value={modelOption.value}>{modelOption.label}</option>
		{/each}
	</select>

	{#if selectedModel === 'custom'}
		<input
			type="text"
			bind:value={customModel}
			placeholder="e.g. mistral:7b"
			class="mt-2 w-full rounded border border-gray-300 p-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
		/>
	{/if}

	<button
		onclick={installNewModel}
		disabled={!newModel || isInstalling || deletingModel !== ''}
		class="mt-3 cursor-pointer rounded bg-blue-300 px-4 py-2 text-black hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-60"
	>
		{#if isInstalling}
			Installing…
		{:else}
			Install
		{/if}
	</button>

	{#if actionError}
		<p class="mt-3 text-sm text-red-600">{actionError}</p>
	{/if}

	<a
		href="https://ollama.com/library"
		target="_blank"
		class="mt-3 block text-xs text-blue-500 hover:underline"
	>
		Browse all models on ollama.com/library ↗
	</a>
</div>
