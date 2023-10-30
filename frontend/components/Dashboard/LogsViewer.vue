<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue' // Import ref from Vue
import { ScrollArea } from '@/components/ui/scroll-area'
import { useLogsStore } from '~/store/logs'
import { storeToRefs } from 'pinia'
import { LogLevels } from '~/types/logs.types'
import { Mouse, ScrollText, ScreenShare, XCircle } from 'lucide-vue-next'
import { useDroneComponentsStore } from '~/store/components'

const logsStore = useLogsStore()
const { logs } = storeToRefs(logsStore)
const { connectionStatus } = storeToRefs(useDroneComponentsStore())
const route = useRoute()

const dotsCount = ref(0)
const dots = computed(() => {
  return '.'.repeat(dotsCount.value)
})
let dotsInterval: NodeJS.Timeout | null = null
onMounted(() => {
  dotsInterval = setInterval(() => {
    dotsCount.value = (dotsCount.value + 1) % 4
  }, 500)
})
onUnmounted(() => {
  clearInterval(dotsInterval!)
})

const scrollToBottom = ref(true)

const openInNewTab = () => {
  window.open('/fullscreen/logs', '_blank')
}

const closeWindow = () => {
  window.close()
}
</script>

<template>
  <div class="rounded-md bg-neutral-900 h-full p-2">
    <ScrollArea
      class="h-full rounded bg-black p-3 overflow-y-auto"
      ref="scrollAreaRef"
      :scroll-to-bottom="scrollToBottom"
    >
      <button
        class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        v-if="route.path !== '/fullscreen/logs'"
        @click="openInNewTab"
      >
        <ScreenShare :size="22" />
      </button>
      <button
        class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        v-else
        @click="closeWindow"
      >
        <XCircle :size="22" />
      </button>
      <button
        class="absolute top-11 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="scrollToBottom = !scrollToBottom"
      >
        <ScrollText v-show="!scrollToBottom" :size="24" />
        <Mouse v-show="scrollToBottom" :size="24" />
      </button>
      <div v-for="(log, i) in logs" :key="i">
        <div class="flex gap-1.5">
          <div
            class="w-2 min-w-[0.5rem] h-2 rounded-full mt-1.5"
            :class="{
              'bg-gray-500': log.level === LogLevels.DEBUG,
              'bg-blue-500': log.level === LogLevels.INFO,
              'bg-orange-500': log.level === LogLevels.WARNING,
              'bg-red-500': log.level === LogLevels.ERROR,
              'bg-red-900': log.level === LogLevels.CRITICAL
            }"
          ></div>
          <div class="text-sm text-neutral-100">{{ log.level }}</div>
          <div class="text-sm text-neutral-100">{{ log.time }}</div>
          <div class="text-sm text-neutral-100">{{ log.message }}</div>
        </div>
      </div>
      <div v-if="connectionStatus.connected && logs.length === 0">
        Waiting for logs{{ dots }}
      </div>
      <div v-if="!connectionStatus.connected">
        Waiting for connection{{ dots }}
      </div>
    </ScrollArea>
  </div>
</template>

<style scoped lang="scss"></style>
