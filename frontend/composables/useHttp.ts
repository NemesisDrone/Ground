import { useUserStore } from '~/store/user'
import axios, { AxiosError } from 'axios'

export const useHttp = () => {
  const config = useRuntimeConfig()
  const http = axios.create({
    baseURL: config.public.API_URL,
    headers: {
      'Content-type': 'application/json'
    }
  })

  http.interceptors.request.use((config) => {
    const token = useCookie('access')
    if (config && config.headers && token.value) {
      config.headers['Authorization'] = `Bearer ${token.value}`
    }

    return config
  })

  http.interceptors.response.use(
    (response) => {
      return response
    },
    async (error) => {
      if (error instanceof AxiosError) {
        const originalRequest = error.config
        console.log(useCookie('refresh').value, error.response?.status)
        if (
          error.response?.status === 401 &&
          // @ts-ignore
          originalRequest.url !== '/api/user/refresh' &&
          // @ts-ignore
          originalRequest.url !== '/api/user/blacklist' &&
          useCookie('refresh').value
        ) {
          await useUserStore().refreshTokens()

          if (useCookie('access').value) {
            // @ts-ignore
            return http(originalRequest)
          } else {
            if (document.location.pathname !== '/?disconnected') {
              await useUserStore().logOut()
              document.location.href = '/?disconnected'
            }
          }
          // @ts-ignore
        } else if (originalRequest.url === '/api/user/refresh') {
          if (document.location.pathname !== '/?disconnected') {
            await useUserStore().logOut()
            document.location.href = '/?disconnected'
          }
        }
      }
      return Promise.reject(error)
    }
  )

  return http
}
