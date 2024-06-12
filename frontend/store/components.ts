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
  imu: DroneComponent
  communicationWebsocket: WebSocketWrapper | null
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
    communicationWebsocket: null,
    gps: {
      status: ComponentsState.STOPPED,
      name: 'GPS',
      description: 'GPS',
      routeSlug: 'gps'
    },
    barometer: {
      status: ComponentsState.NOT_EXPECTED,
      name: 'Barometer',
      description: 'Barometer'
    },
    batteryReader: {
      status: ComponentsState.STOPPED,
      name: 'Battery',
      description: 'Battery reader',
      routeSlug: 'battery'
    },
    propulsionController: {
      status: ComponentsState.NOT_EXPECTED,
      name: 'Propulsion',
      description: 'Propulsion controller',
      speed: 0
    },
    servoController: {
      status: ComponentsState.NOT_EXPECTED,
      name: 'Servo',
      description: 'Servo controller'
    },
    imu: {
      status: ComponentsState.STOPPED,
      name: 'IMU',
      description: 'Inertial measurement unit',
      routeSlug: 'imu'
    },
    laserDistanceSensor: {
      status: ComponentsState.NOT_EXPECTED,
      name: 'Laser',
      description: 'Laser distance sensor',
      routeSlug: 'laser-distance'
    },
    connectionStatus: {
      connected: false
    },
    controller: {
      status: ComponentsState.NOT_EXPECTED,
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
