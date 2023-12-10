<script setup lang="ts">
import { WebSocketWrapper } from '~/helpers/webSocketWrapper'
import { useSensorsStore } from '~/store/sensors'
import { useLogsStore } from '~/store/logs'
import { useComponentsStore } from '~/store/components'
import { useGamepadController } from '~/composables/useGamePadController'
import {
  Menu,
  KanbanSquare,
  View,
  Settings,
  Camera
} from 'lucide-vue-next'
import { useDroneSettingsStore } from '~/store/droneSettings'

let ws: WebSocketWrapper | null = null
const droneStore = useComponentsStore()
const sensorsStore = useSensorsStore()
const logsStore = useLogsStore()

let controllerAxesInterval: NodeJS.Timeout | null = null
let controllerButtonsInterval: NodeJS.Timeout | null = null
onMounted(() => {
  /**
   * Create a new WebSocketWrapper instance
   * and provide it to the whole application
   * Add callbacks to handle incoming messages
   */
  ws = new WebSocketWrapper(
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
  ws.onMessage('sensors:full', (event) => {
    sensorsStore.full = event.data
  })
  ws.onMessage('log', (event) => {
    logsStore.logs.push(event.data)
    if (logsStore.logs.length > 1000) logsStore.logs.splice(0, 200)
  })
  ws.onMessage('drone:connection-status', (event) => {
    droneStore.connectionStatus = event.data
  })
  droneStore.websocket = ws

  const { controllerGetAxesInterval, controllerGetButtonsInterval } =
    useGamepadController()
  controllerAxesInterval = controllerGetAxesInterval
  controllerButtonsInterval = controllerGetButtonsInterval
})

onUnmounted(() => {
  ws?.close()

  if (controllerAxesInterval) clearInterval(controllerAxesInterval)
  if (controllerButtonsInterval) clearInterval(controllerButtonsInterval)
})

const route = useRoute()

const dashboardLayouts = [
  {
    icon: KanbanSquare,
    title: 'Dashboard',
    route: '/operations/dashboard'
  },
  {
    icon: View,
    title: 'Map & Video',
    route: '/operations/map-video'
  },
  {
    icon: Camera,
    title: 'Monitoring',
    route: '/operations/monitoring'
  }
]
</script>

<template>
  <div class="flex">
    <div
      class="w-[62px] h-[100vh] border-r-2 border-neutral-900 flex flex-col items-center justify-between fixed"
    >
      <div class="flex flex-col gap-2 mt-[1.5rem]">
        <router-link
          v-for="dashboardLayout in dashboardLayouts"
          class="cursor-pointer"
          :class="{
            'text-primary': route.path === dashboardLayout.route
          }"
          :title="dashboardLayout.title"
          :to="dashboardLayout.route"
        >
          <component :is="dashboardLayout.icon" :size="28" />
        </router-link>
      </div>
      <div class="mb-4">
        <router-link
          class="cursor-pointer"
          :class="{
            'text-primary': route.path === '/operations/settings'
          }"
          to="/operations/settings"
        >
          <Settings :size="28" />
        </router-link>
      </div>
    </div>
    <main class="w-full ml-[62px]">
      <slot />
    </main>
  </div>
</template>

<style scoped lang="scss"></style>
