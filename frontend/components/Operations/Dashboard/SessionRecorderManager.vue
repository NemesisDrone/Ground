<script setup lang="ts">
import { PlayCircle } from 'lucide-vue-next'
import { useComponentsStore } from '~/store/components'

const componentsStore = useComponentsStore()

const pauseReplay = () => {
  componentsStore.communicationWebsocket?.send({
    route: 'record:pause',
    data: null
  })
}
const startRecord = () => {
  componentsStore.communicationWebsocket?.send({
    route: 'record:start',
    data: null
  })
}

const stopRecord = () => {
  componentsStore.communicationWebsocket?.send({
    route: 'record:stop',
    data: null
  })
}
</script>

<template>
  <div class="rounded bg-neutral-900 h-full p-4 flex flex-col">
    <h4>Session recorder</h4>
    <div class="flex mt-2 justify-between items-center">
      <UiButton @click="startRecord">
        <span class="flex items-center gap-2">
          <PlayCircle :size="20" />
          <span>Start</span>
        </span>
      </UiButton>
      <div>
        <span class="text-red-600">Currently not recording</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss"></style>
