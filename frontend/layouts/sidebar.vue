<script setup lang="ts">
import { useGamepadController } from '~/composables/useGamePadController'
import {
  KanbanSquare,
  View,
  Settings,
  Camera,
  Repeat1
} from 'lucide-vue-next'
import { useCommunicationWebsocket } from '~/composables/communicationWebsocket'

const { close: closeCommunicationWebSocket } = useCommunicationWebsocket()

let controllerAxesInterval: NodeJS.Timeout | null = null
let controllerButtonsInterval: NodeJS.Timeout | null = null

onMounted(() => {
  const { controllerGetAxesInterval, controllerGetButtonsInterval } =
    useGamepadController()
  controllerAxesInterval = controllerGetAxesInterval
  controllerButtonsInterval = controllerGetButtonsInterval
})

onUnmounted(() => {
  closeCommunicationWebSocket()

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
  },
  {
    icon: Repeat1,
    title: 'Replay',
    route: '/operations/replay'
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
      <div>
        <slot />
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss"></style>
