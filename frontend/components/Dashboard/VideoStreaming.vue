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
      class="w-full h-full object-cover"
      src="https://media.tenor.com/UuLJ3JKB_PQAAAAd/bomb-explosion.gif"
    />

    <ScreenShare
      v-if="route.path !== '/fullscreen/video'"
      class="absolute top-0 right-0 m-2 cursor-pointer"
      color="black"
      :size="24"
      @click="openInNewTab"
    />
    <XCircle
      v-else
      class="absolute top-0 right-0 m-3 cursor-pointer"
      color="black"
      :size="32"
      @click="closeWindow"
    />
  </div>
</template>

<style scoped lang="scss"></style>
