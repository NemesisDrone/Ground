import { defineStore, acceptHMRUpdate } from 'pinia'

export const useSensorsStore = defineStore('sensors', {
  state: () => ({
    altitude: 0,
    gpsPosition: {
      lat: 0,
      lng: 0
    },
    battery: 0,
    speed: 0
  })
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSensorsStore, import.meta.hot))
}
