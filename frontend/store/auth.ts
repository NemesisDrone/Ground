import { defineStore, acceptHMRUpdate } from 'pinia'

interface UserLoginPayload {
  identifier: string
  password: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    authenticated: false,
    loading: false
  }),
  actions: {
    async authenticateUser({ identifier, password }: UserLoginPayload) {
      this.loading = true
      const { data } = await useApi<
        {
          access: string
          refresh: string
        },
        any
      >('/api/user/token', {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: {
          identifier,
          password
        }
      })
      this.loading = false

      if (data.value?.access && data.value?.refresh) {
        const access = useCookie('access')
        access.value = data.value.access

        const refresh = useCookie('refresh')
        refresh.value = data.value.refresh

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
      const { data } = await useApi('/api/user/blacklist', {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: {
          refresh
        }
      })

      token.value = null
      refresh.value = null
      this.authenticated = false
    }
  },
  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
}
