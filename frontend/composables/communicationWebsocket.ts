import { WebSocketWrapper } from '~/helpers/webSocketWrapper'
import { useComponentsStore } from '~/store/components'
import { useSensorsStore } from '~/store/sensors'
import { useLogsStore } from '~/store/logs'

/**
 * Create a new WebSocketWrapper instance
 * and provide it to the whole application
 * Add callbacks to handle incoming messages
 */
export const useCommunicationWebsocket = () => {
  const droneStore = useComponentsStore()
  const sensorsStore = useSensorsStore()
  const logsStore = useLogsStore()
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
  ws.onMessage('sensors:sense_hat:data', (event) => {
    sensorsStore.full = event.data
  })
  ws.onMessage('log', (event) => {
    logsStore.logs.push(event.data)
    if (logsStore.logs.length > 1000) logsStore.logs.splice(0, 200)
  })
  ws.onMessage('drone:connection-status', (event) => {
    droneStore.connectionStatus = event.data
  })
  droneStore.communicationWebsocket = ws

  const close = () => {
    ws.close()
    droneStore.communicationWebsocket = null
  }

  return { ws, close }
}
