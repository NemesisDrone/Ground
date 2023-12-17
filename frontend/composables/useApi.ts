import { useUserStore } from '~/store/user'
import { NitroFetchOptions, NitroFetchRequest } from 'nitropack'

export const useApi = async <T>(
  request: NitroFetchRequest,
  opts?: NitroFetchOptions<string>
): Promise<T> => {
  const config = useRuntimeConfig()

  return $fetch(request, {
    baseURL: config.public.API_URL,
    ...opts,
    onRequest({ options }) {
      const token = useCookie('access')
      if (token.value) {
        if (!options.headers) options.headers = {}

        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token.value}`
        }
      }
    },
    async onResponseError({ response, options }) {
      if (
        response.status === 401 &&
        !response.url.includes('/api/user/token')
      ) {
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
