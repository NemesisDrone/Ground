// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  runtimeConfig: {
    public: {
      API_URL: process.env.API_URL,
      WEB_SOCKET_COMMUNICATION_URL:
        process.env.WEB_SOCKET_COMMUNICATION_URL,
      NVS_WEB_SOCKET_URL: process.env.NVS_WEB_SOCKET_URL
    }
  },
  modules: [
    '@nuxtjs/tailwindcss',
    'nuxt-particles',
    'nuxt-mapbox',
    '@pinia/nuxt',
    '@tresjs/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
    [
      '@nuxtjs/google-fonts',
      {
        families: {
          Roboto: true
        }
      }
    ]
  ],
  pinia: {
    autoImports: ['defineStore', ['defineStore', 'definePiniaStore']]
  },
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
  ],
  ssr: false
})
