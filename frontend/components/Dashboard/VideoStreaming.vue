<script setup lang="ts">
import { ScreenShare, XCircle } from 'lucide-vue-next'

const route = useRoute()

const openInNewTab = () => {
  window.open('/fullscreen/video', '_blank')
}

const closeWindow = () => {
  window.close()
}
</script>

<template>
  <div class="relative h-full m-0 p-0 overflow-hidden">
    <img
      class="w-full object-cover h-full"
      src="https://media.tenor.com/UuLJ3JKB_PQAAAAd/bomb-explosion.gif"
    />
    <button
      class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
      v-if="route.path !== '/fullscreen/video'"
      @click="openInNewTab"
      title="Open in new tab"
    >
      <ScreenShare :size="24" />
    </button>
    <button
      class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
      v-else
      @click="closeWindow"
      title="Close window"
    >
      <XCircle :size="32" />
    </button>
  </div>
</template>

<style scoped lang="scss"></style>
