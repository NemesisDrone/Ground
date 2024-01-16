import { useUserStore } from '~/store/user'
import axios, { AxiosError } from 'axios'

export const useHttp = () => {
  const config = useRuntimeConfig()
  const userStore = useUserStore()
  const http = axios.create({
    baseURL: config.public.API_URL,
    headers: {
      'Content-type': 'application/json'
    }
  })

  http.interceptors.request.use((config) => {
    if (config && config.headers && userStore.accessToken) {
      config.headers['Authorization'] = `Bearer ${userStore.accessToken}`
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
        // Prevent infinite loops
        // @ts-ignore Property '_retry' does not exist on type 'AxiosRequestConfig'.
        if (originalRequest._retry) {
          await useUserStore().logOut()
          document.location.href = '/?disconnected'
        }
        // @ts-ignore
        originalRequest._retry = true

        if (
          error.response?.status === 401 &&
          // TODO: refacto this shit
          originalRequest?.url !== '/api/user/refresh' &&
          originalRequest?.url !== '/api/user/blacklist' &&
          originalRequest?.url !== '/api/user/token' &&
          userStore.refreshToken
        ) {
          await userStore.refreshExpiredToken()

          if (userStore.accessToken) {
            // @ts-ignore
            return await http(originalRequest)
          } else {
            if (document.location.pathname !== '/?disconnected') {
              await useUserStore().logOut()
              document.location.href = '/?disconnected'
            }
          }
        } else if (originalRequest?.url === '/api/user/refresh') {
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
