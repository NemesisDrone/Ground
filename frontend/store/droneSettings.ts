import { defineStore, acceptHMRUpdate } from 'pinia'
import { useComponentsStore } from '~/store/components'

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
    async sendDroneConfig() {
      const ws = useComponentsStore().websocket
      if (ws) {
        ws.send({
          route: 'config',
          data: {
            canals: this.canals
          }
        })
      }
    },

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
      this.sendDroneConfig()
    }
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useDroneSettingsStore, import.meta.hot)
  )
}
