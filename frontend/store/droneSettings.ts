import { defineStore, acceptHMRUpdate } from 'pinia'
import { useComponentsStore } from '~/store/components'
import { Model } from '~/types/droneSettings.types'
interface State {
  id: number
  models: Model[]
  selected_drone_model: {
    name: string
    id: number
  }
}

export const useDroneSettingsStore = defineStore('droneSettings', {
  state: (): State => ({
    id: -1,
    models: [],
    selected_drone_model: {
      name: 'No model selected',
      id: -1
    }
  }),

  actions: {
    async sendDroneConfig() {
      const ws = useComponentsStore().communicationWebsocket
      if (ws) {
        ws.send({
          route: 'config',
          data: {}
        })
      }
    },

    async getSettings() {
      const { data } = await useHttp().get<{
        id: number
        models: Model[]
        selected_drone_model: {
          name: string
          id: number
        }
      }>('/api/drone/settings/')
      this.id = data.id
      this.models = data.models
      this.selected_drone_model = data.selected_drone_model
    },

    async updateSelectedDroneModel(id: number) {
      const { data } = await useHttp().post<{
        id: number
        models: Model[]
        selected_drone_model: {
          name: string
          id: number
        }
      }>('/api/drone/settings/select-model/', {
        selected_drone_model: id
      })

      this.models = data.models
      this.selected_drone_model = data.selected_drone_model
    },

    async createDroneModel(model: Model) {
      const { data } = await useHttp().post<Model>(
        '/api/drone/settings/models/',
        model
      )
    },

    async updateDroneModel(model: Model) {
      const { data } = await useHttp().put<Model>(
        `/api/drone/settings/models/${model.id}/`,
        model
      )
    },

    async deleteDroneModel(id: number) {
      const { data } = await useHttp().delete<Model>(
        `/api/drone/settings/models/${id}/`
      )
    }
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useDroneSettingsStore, import.meta.hot)
  )
}
