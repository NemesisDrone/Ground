import { defineStore, acceptHMRUpdate } from 'pinia'

export const useSensorsStore = defineStore('sensors', {
  state: () => ({
    altitude: 20,
    gpsPosition: {
      lat: -0.7563779,
      lng: 48.0879123
    },
    battery: 0,
    speed: 0,
    full: {
      timestamp: 0,
      roll: 0,
      pitch: 0,
      yaw: 0,
      gyroRoll: 0,
      gyroPitch: 0,
      gyroYaw: 0,
      accelX: 0,
      accelY: 0,
      accelZ: 0,
      compassX: 0,
      compassY: 0,
      compassZ: 0,
      pressure: 0,
      temperature: 0,
      humidity: 0
    }
  })
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSensorsStore, import.meta.hot))
}
