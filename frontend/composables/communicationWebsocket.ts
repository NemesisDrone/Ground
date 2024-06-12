import { WebSocketWrapper } from '~/helpers/webSocketWrapper'
import { useComponentsStore } from '~/store/components'
import { useSensorsStore } from '~/store/sensors'
import { useLogsStore } from '~/store/logs'
import { useReplayStore } from '~/store/replayStore'
import { ComponentsState, DroneComponent } from '~/types/components.types'

/**
 * Create a new WebSocketWrapper instance
 * and provide it to the whole application
 * Add callbacks to handle incoming messages
 */
export const useCommunicationWebsocket = () => {
  const droneStore = useComponentsStore()
  const sensorsStore = useSensorsStore()
  const logsStore = useLogsStore()
  const replayStore = useReplayStore()
  const ws = new WebSocketWrapper(
    useRuntimeConfig().public.WEB_SOCKET_COMMUNICATION_URL as string
  )
  ws.onMessage('sensors:altitude', (event) => {
    sensorsStore.altitude = event.data
  })

  ws.onMessage('sensors:battery', (event) => {
    sensorsStore.battery = event.data
  })

  ws.onMessage('sensors:speed', (event) => {
    sensorsStore.speed = event.data
  })

  ws.onMessage('sensors:gps', (event) => {
    sensorsStore.gpsPosition = event.data
  })

  ws.onMessage('sensors:imu:data', (event) => {
    sensorsStore.imu = event.data
  })

  ws.onMessage('log', (event) => {
    logsStore.logs.push(event.data)
    if (logsStore.logs.length > 1000) logsStore.logs.splice(0, 200)
  })

  ws.onMessage('drone:connection-status', (event) => {
    droneStore.connectionStatus = event.data
  })
  droneStore.communicationWebsocket = ws

  ws.onMessage('drone:status', (event) => {
    // Not nice, but i don't have time to refactor this
    for (const key in event.data) {
      // @ts-ignore
      if (event.data[key] == 'started') {
        // @ts-ignore
        droneStore[key].status = ComponentsState.STARTED
      } else {
        // @ts-ignore
        droneStore[key].status = ComponentsState.STOPPED
      }
    }
  })

  const close = () => {
    ws.close()
    droneStore.communicationWebsocket = null
  }

  return { ws, close }
}
