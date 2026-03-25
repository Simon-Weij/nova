<script>
	import { goto } from '$app/navigation';

	import { password as passwordStore } from '$lib/store'

	let password = $state('');
	let error = $state('');
	let isLoggingIn = $state(false);

	async function login() {
		if (!password.trim()) {
			error = 'Password is required';
			return;
		}

		isLoggingIn = true;
		error = '';
		passwordStore.set(password);

		const res = await fetch('/api/auth/check', {
			headers: {
				'x-api-key': password
			}
		});

		if (res.ok) {
			await goto('/dashboard');
		} else {
			error = 'Invalid password. Please try again.';
		}

		isLoggingIn = false;
	}
</script>

<main class="flex min-h-screen w-full items-center justify-center bg-[#ADD8E6] px-4">
	<div class="w-full max-w-md rounded-3xl bg-white px-6 py-8 text-center shadow shadow-black">
		<h1 class="text-lg font-bold">Nova Login</h1>
		<p class="mt-1 mb-4 text-sm text-gray-600">Enter the password configured in your `.env`</p>
		{#if error}
			<p class="mb-3 text-sm text-red-500">{error}</p>
		{/if}
		<input
			type="password"
			bind:value={password}
			class="mb-3 w-full rounded border border-gray-300 p-3 shadow focus:ring-2 focus:ring-blue-500 focus:outline-none"
			placeholder="Password"
			onkeydown={(event) => event.key === 'Enter' && login()}
		/>
		<button class="w-full cursor-pointer rounded bg-blue-300 px-6 py-3" onclick={login} disabled={isLoggingIn}>
			{#if isLoggingIn}
				Logging in...
			{:else}
				Login
			{/if}
		</button>
	</div>
</main>
