<script setup lang="ts">
import { WebSocketWrapper } from '~/helpers/webSocketWrapper'
import { useSensorsStore } from '~/store/sensors'
import { useLogsStore } from '~/store/logs'
import { useDroneComponentsStore } from '~/store/droneComponents'

let ws: WebSocketWrapper | null = null
const droneStore = useDroneComponentsStore()
const sensorsStore = useSensorsStore()
const logsStore = useLogsStore()
onMounted(() => {
  /**
   * Create a new WebSocketWrapper instance
   * and provide it to the whole application
   * Add callbacks to handle incoming messages
   */
  ws = new WebSocketWrapper(
    useRuntimeConfig().public.WEB_SOCKET_COMMUNICATION_URL as string
  )
  ws.onMessage('sensor:altitude', (event) => {
    sensorsStore.altitude = event.data
  })
  ws.onMessage('sensor:battery', (event) => {
    sensorsStore.battery = event.data
  })
  ws.onMessage('sensor:speed', (event) => {
    sensorsStore.speed = event.data
  })
  ws.onMessage('log', (event) => {
    logsStore.logs.push(event.data)
    if (logsStore.logs.length > 1000) logsStore.logs.splice(0, 200)
  })
  droneStore.websocket = ws
})

onUnmounted(() => {
  ws?.close()
})
</script>

<template>
  <div>
    <slot />
  </div>
</template>

<style scoped lang="scss"></style>
