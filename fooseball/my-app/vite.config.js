import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import importAssets from 'svelte-preprocess-import-assets'
// https://vitejs.dev/config/
export default defineConfig({
  preprocess: [importAssets()],
  plugins: [svelte()]
})
