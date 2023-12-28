import { defineStore, acceptHMRUpdate } from 'pinia'
import { UserData } from '~/types/user.types'

interface UserLoginPayload {
  identifier: string
  password: string
}

export const useUserStore = defineStore('user', {
  state: () => ({
    authenticated: false,
    user: null as null | UserData
  }),
  actions: {
    async getUserData() {
      const { data } = await useHttp().get<UserData>('/api/user/data')
      if (data) {
        this.user = data
      }
    },

    async authenticateUser({ identifier, password }: UserLoginPayload) {
      const { data } = await useHttp().post<{
        access: string
        refresh: string
      }>('/api/user/token', {
        identifier,
        password
      })

      if (data.access && data.refresh) {
        const access = useCookie('access')
        access.value = data.access

        const refresh = useCookie('refresh')
        refresh.value = data.refresh

        this.authenticated = true
      } else {
        this.authenticated = false
        const access = useCookie('access')
        access.value = null

        const refresh = useCookie('refresh')
        refresh.value = null
      }
    },

    async logOut() {
      const token = useCookie('token')
      const refresh = useCookie('refresh')
      // await useHttp().post('/api/user/blacklist', {
      //   refresh: refresh.value,
      //   token: token.value
      // })

      token.value = null
      refresh.value = null
      this.authenticated = false
    },

    async refreshTokens() {
      const refresh = useCookie('refresh')
      const accessCookie = useCookie('access')

      try {
        const { data } = await useHttp().post<{
          access: string
        }>('/api/user/refresh', {
          refresh: refresh.value
        })

        if (data.access) {
          accessCookie.value = data.access

          this.authenticated = true
        } else {
          this.authenticated = false
          accessCookie.value = null
          refresh.value = null
        }
      } catch (e) {
        this.authenticated = false
        accessCookie.value = null
        refresh.value = null
      }
    }
  },
  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot))
}
