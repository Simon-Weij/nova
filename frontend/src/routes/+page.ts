import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
  const res = await fetch('/api/settings/get');
  if (res.status === 404) {
    redirect(307, '/setup');
  } else {
    redirect(307, '/dashboard')
  }
};