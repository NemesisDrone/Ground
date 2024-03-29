import { acceptHMRUpdate, defineStore } from 'pinia'
import { Model } from '~/types/droneSettings.types'

interface State {
  id: number
  models: Model[]
  selected_drone_model: {
    name: string
    id: number
  }
  objectives: {
    droneDirection: {
      lat: number
      lng: number
    }
    altitude: number
  }
}

export const useDroneSettingsStore = defineStore('droneSettings', {
  state: (): State => ({
    id: -1,
    models: [],
    selected_drone_model: {
      name: 'No model selected',
      id: -1
    },
    objectives: {
      droneDirection: {
        lat: 0,
        lng: 0
      },
      altitude: 100
    }
  }),

  actions: {
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

    async updateDroneObjectives() {
      await useHttp().post('/api/drone/settings/objectives/', {
        altitude_objective: this.objectives.altitude,
        latitude_objective: this.objectives.droneDirection.lat,
        longitude_objective: this.objectives.droneDirection.lng
      })
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
