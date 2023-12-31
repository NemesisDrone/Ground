import { defineStore, acceptHMRUpdate } from 'pinia'
import { DroneImage } from '~/types/images.types'
import { useComponentsStore } from '~/store/components'

interface State {
  images: DroneImage[]
}

export const useMonitoringStore = defineStore('monitoring', {
  state: (): State => ({
    images: []
  }),

  actions: {
    async takePicture() {
      const ws = useComponentsStore().websocket
      if (ws) {
        ws.send({
          route: 'take-picture',
          data: {}
        })
      }
    },

    async getImages() {
      const { data } = await useHttp().get<DroneImage[]>(
        '/api/drone/images/'
      )

      this.images = data
    },

    async deleteImage(deletedImage: DroneImage) {
      await useHttp().delete(`/api/drone/images/${deletedImage.id}/`)
      this.images = this.images.filter(
        (image) => image.id !== deletedImage.id
      )
    }
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useMonitoringStore, import.meta.hot)
  )
}
