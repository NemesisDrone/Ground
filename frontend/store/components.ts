import { defineStore, acceptHMRUpdate } from 'pinia'
import { ComponentsState, DroneComponent } from '~/types/components.types'
import { WebSocketWrapper } from '~/helpers/webSocketWrapper'
interface State {
  gps: DroneComponent
  barometer: DroneComponent
  batteryReader: DroneComponent
  propulsionController: {
    status: ComponentsState
    name: string
    description: string
    speed: number
  }
  servoController: DroneComponent
  websocket: WebSocketWrapper | null
  connectionStatus: {
    connected: boolean
  }
  laserDistanceSensor: DroneComponent
  controller: {
    status: ComponentsState
    name: string
    description: string
    controllerId: number | null
    disableActions: boolean
    axes: {
      pitch: number
      roll: number
    }
  }
}

export const useComponentsStore = defineStore('components', {
  state: (): State => ({
    websocket: null,
    gps: {
      status: ComponentsState.STOPPED,
      name: 'GPS',
      description: 'GPS',
      routeSlug: 'gps'
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
      description: 'Propulsion controller',
      speed: 0
    },
    servoController: {
      status: ComponentsState.STOPPED,
      name: 'Servo',
      description: 'Servo controller'
    },
    laserDistanceSensor: {
      status: ComponentsState.STOPPED,
      name: 'Laser',
      description: 'Laser distance sensor',
      routeSlug: 'laser-distance'
    },
    connectionStatus: {
      connected: false
    },
    controller: {
      status: ComponentsState.STOPPED,
      name: 'Controller',
      description: 'Gamepad controller',
      disableActions: true,
      controllerId: null,
      axes: {
        pitch: 0,
        roll: 0
      }
    }
  })
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useComponentsStore, import.meta.hot)
  )
}
