<script lang="ts" setup>
import GPSMap from '~/components/Dashboard/GPSMap.vue'
import VideoStreaming from '~/components/Dashboard/VideoStreaming.vue'
import SpeedGauge from '~/components/Dashboard/SpeedGauge.vue'
import Altitude from '~/components/Dashboard/Altitude.vue'
import Battery from '~/components/Dashboard/Battery.vue'
import PropulsorSpeed from '~/components/Dashboard/PropulsorSpeed.vue'
import Camera from '~/components/Dashboard/Camera.vue'
import { WebSocketWrapper } from '~/helpers/webSocketWrapper'
import { useSensorsStore } from '~/store/sensors'

let ws: WebSocketWrapper | null = null
const sensorsStore = useSensorsStore()
onMounted(() => {
  /**
   * Create a new WebSocketWrapper instance
   * and provide it to the whole application
   * Add callbacks to handle incoming messages
   */
  ws = new WebSocketWrapper(
    useRuntimeConfig().public.WEB_SOCKET_COMMUNICATION_URL as string
  )
  console.log(ws, 'aa')

  ws.onMessage('sensors.altitude', (event) => {
    sensorsStore.altitude = event.data
  })
  ws.onMessage('sensors.battery', (event) => {
    sensorsStore.battery = event.data
  })
  ws.onMessage('sensors.speed', (event) => {
    sensorsStore.speed = event.data
  })
})

onUnmounted(() => {
  ws?.close()
})

const send = () => {
  ws?.send({ message: 'Hello', test: 'aa' })
}
</script>

<template>
  <div class="w-full h-full flex min-h-[100vh]">
    <div class="w-3/5 p-4">
      <div class="w-full h-1/6 flex gap-4">
        <div class="w-full h-full">
          <SpeedGauge />
        </div>
        <div class="w-full h-full">
          <Altitude />
        </div>
        <div class="w-full h-full">
          <Battery />
        </div>
        <div class="w-full h-full">
          <PropulsorSpeed />
        </div>
        <div class="w-full h-full">
          <Camera />
        </div>
      </div>

      <UiButton class="mt-7" @click="send">test</UiButton>
    </div>
    <div class="w-2/5 p-2">
      <div class="w-full h-1/2 pb-1">
        <GPSMap />
      </div>
      <div class="w-full h-1/2 pt-1">
        <VideoStreaming />
      </div>
    </div>
  </div>
</template>

<style lang="scss"></style>
