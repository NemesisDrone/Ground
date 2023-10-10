// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  app: {
    pageTransition: { name: 'page', mode: 'out-in' }
  },
  modules: [
    '@nuxtjs/tailwindcss',
    'nuxt-particles',
    'nuxt-mapbox',
    '@pinia/nuxt'
  ],
  // @ts-ignore
  pinia: {
    autoImports: ['defineStore', ['defineStore', 'definePiniaStore']]
  },
  // @ts-ignore
  mapbox: {
    accessToken:
      'pk.eyJ1IjoieHBpZXJyZSIsImEiOiJjbG05anh5NW8wa3pkM3BvNTd6NTZ1Z2czIn0.8BcNWxnR7ru-MIyy6Y8-Tg'
  },
  components: [
    {
      path: '~/components/ui',
      extensions: ['.vue'],
      prefix: 'Ui'
    }
  ]
})
