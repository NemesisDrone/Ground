import { defineStore, acceptHMRUpdate } from 'pinia'

type Canal = {
  canal: number
  gpios: number[]
}

interface State {
  canals: Canal[]
}

export const useDroneSettingsStore = defineStore('droneSettings', {
  state: (): State => ({
    canals: []
  }),

  actions: {
    async getSettings() {
      const data = await useApi<{
        id: number
        canals: Canal[]
      }>('/api/drone/settings/')

      this.canals = data.canals
    },

    async updateSettings({ canals }: { canals: Canal[] }) {
      const data = await useApi<{
        id: number
        canals: Canal[]
      }>('/api/drone/settings/update/', {
        method: 'POST',
        body: {
          canals
        }
      })

      this.canals = data.canals
    }
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useDroneSettingsStore, import.meta.hot)
  )
}
