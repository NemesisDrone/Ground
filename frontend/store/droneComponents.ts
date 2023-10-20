import { defineStore, acceptHMRUpdate } from 'pinia'
import { ComponentsState, DroneComponent } from '~/types/components.types'

interface State {
  gps: DroneComponent
  barometer: DroneComponent
  batteryReader: DroneComponent
  propulsionController: DroneComponent
  servoController: DroneComponent
}

export const useDroneComponentsStore = defineStore('droneComponents', {
  state: () => ({
    gps: {
      status: ComponentsState.STOPPED,
      name: 'GPS',
      description: 'GPS'
    },
    barometer: {
      status: ComponentsState.RUNNING,
      name: 'Barometer',
      description: 'Barometer'
    },
    batteryReader: {
      status: ComponentsState.RUNNING,
      name: 'Battery',
      description: 'Battery reader'
    },
    propulsionController: {
      status: ComponentsState.ERROR,
      name: 'Propulsion',
      description: 'Propulsion controller'
    },
    servoController: {
      status: ComponentsState.RUNNING,
      name: 'Servo',
      description: 'Servo controller'
    }
  })
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useDroneComponentsStore, import.meta.hot)
  )
}
