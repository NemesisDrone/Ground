import { defineStore, acceptHMRUpdate } from 'pinia'
import { UserData } from '~/types/user.types'

interface UserLoginPayload {
  identifier: string
  password: string
}

export const useUserStore = defineStore('user', {
  state: () => ({
    authenticated: false,
    user: null as null | UserData,
    accessToken: null as null | string,
    refreshToken: null as null | string
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
        this.accessToken = data.access
        this.refreshToken = data.refresh

        this.authenticated = true
      } else {
        this.authenticated = false
        this.accessToken = null
        this.refreshToken = null
      }
    },

    async logOut() {
      // await useHttp().post('/api/user/blacklist', {
      //   refresh: refresh.value,
      //   token: token.value
      // })

      this.accessToken = null
      this.refreshToken = null
      this.authenticated = false
    },

    async refreshExpiredToken() {
      try {
        const { data } = await useHttp().post<{
          access: string
        }>('/api/user/refresh', {
          refresh: this.refreshToken
        })

        if (data.access) {
          this.accessToken = data.access

          this.authenticated = true
        } else {
          this.authenticated = false
          this.accessToken = null
          this.refreshToken = null
        }
      } catch (e) {
        this.authenticated = false
        this.accessToken = null
        this.refreshToken = null
      }
    }
  },
  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot))
}
