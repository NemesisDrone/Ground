import { useUserStore } from '~/store/user'

export const useApi: typeof useFetch = (request, opts?) => {
  const config = useRuntimeConfig()

  // @ts-ignore
  return useFetch(request, {
    baseURL: config.public.API_URL,
    ...opts,
    async onRequest({ request, options }) {
      const token = useCookie('access')
      if (token.value) {
        if (!options.headers) options.headers = {}
        // @ts-ignore
        options.headers.Authorization = `Bearer ${token.value}`
      }
    },
    // @ts-ignore
    async onResponseError({ request, response, options }) {
      if (response.status === 401) {
        const userStore = useUserStore()
        if (useCookie('refresh').value) {
          await userStore.refreshTokens()
          // @ts-ignore
          return useApi(request, options)
        }
      }
    }
  })
}
