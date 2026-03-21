import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
  const res = await fetch('/api/settings/status');
  if (!res.ok) {
    redirect(307, '/setup');
  } else {
    redirect(307, '/dashboard');
  }
};