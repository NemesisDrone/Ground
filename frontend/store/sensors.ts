import { defineStore, acceptHMRUpdate } from 'pinia'
import { MathUtils } from 'three'

export const useSensorsStore = defineStore('sensors', {
  state: () => ({
    altitude: 100,
    gpsPosition: {
      lat: -0.7563779,
      lng: 48.0879123
    },
    battery: 0,
    speed: 0,
    imu: {
      roll: 0,
      pitch: 0,
      yaw: 90,
      quat: [] as number[]
    }
  })
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSensorsStore, import.meta.hot))
}
