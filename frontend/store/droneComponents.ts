import { defineStore, acceptHMRUpdate } from 'pinia'
import { ComponentsState, DroneComponent } from '~/types/components.types'
import { WebSocketWrapper } from '~/helpers/webSocketWrapper'

interface State {
  gps: DroneComponent
  barometer: DroneComponent
  batteryReader: DroneComponent
  propulsionController: DroneComponent
  servoController: DroneComponent
  websocket: WebSocketWrapper | null
  connectionStatus: {
    connected: boolean
  }
}

export const useDroneComponentsStore = defineStore('droneComponents', {
  state: (): State => ({
    websocket: null,
    gps: {
      status: ComponentsState.STOPPED,
      name: 'GPS',
      description: 'GPS'
    },
    barometer: {
      status: ComponentsState.STOPPED,
      name: 'Barometer',
      description: 'Barometer'
    },
    batteryReader: {
      status: ComponentsState.STOPPED,
      name: 'Battery',
      description: 'Battery reader'
    },
    propulsionController: {
      status: ComponentsState.STOPPED,
      name: 'Propulsion',
      description: 'Propulsion controller'
    },
    servoController: {
      status: ComponentsState.STOPPED,
      name: 'Servo',
      description: 'Servo controller'
    },
    connectionStatus: {
      connected: false
    }
  })
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useDroneComponentsStore, import.meta.hot)
  )
}
