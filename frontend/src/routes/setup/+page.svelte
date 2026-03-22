<script>
	import { goto } from '$app/navigation';

	import { password as passwordStore } from '$lib/store'

	let password = $state('');
	let confirm = $state('');
	let error = $state('');

	async function setPassword() {
		if (password !== confirm) {
			error = 'Passwords do not match';
			return;
		}

		passwordStore.set(password)

		const res = await fetch('/api/settings/upload', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ password })
		});

		if (res.ok) {
			await goto('/dashboard');
		} else {
			error = 'Something went wrong. Please try again.';
		}
	}
</script>

<main class="flex min-h-screen w-full items-center justify-center bg-[#ADD8E6] px-4">
	<div class="w-full max-w-md rounded-3xl bg-white px-6 py-8 text-center shadow shadow-black">
		<h1 class="text-lg font-bold">Initial setup</h1>
		<p class="mt-1 mb-4 text-sm text-gray-600">To get started, set a password for nova</p>
		{#if error}
			<p class="mb-3 text-sm text-red-500">{error}</p>
		{/if}
		<input
			type="password"
			bind:value={password}
			class="mb-3 w-full rounded border border-gray-300 p-3 shadow focus:ring-2 focus:ring-blue-500 focus:outline-none"
			placeholder="Password"
		/>
		<input
			type="password"
			bind:value={confirm}
			class="mb-3 w-full rounded border border-gray-300 p-3 shadow focus:ring-2 focus:ring-blue-500 focus:outline-none"
			placeholder="Confirm password"
		/>
		<button class="w-full cursor-pointer rounded bg-blue-300 px-6 py-3" onclick={setPassword}>
			Confirm
		</button>
	</div>
</main>
