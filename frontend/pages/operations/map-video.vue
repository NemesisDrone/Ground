<script lang="ts" setup>
import GPSMap from '~/components/Operations/Dashboard/GPSMap.vue'
import VideoStreaming from '~/components/Operations/Dashboard/VideoStreaming.vue'

definePageMeta({
  layout: 'sidebar',
  keepalive: false
})
useHead({
  title: 'Map & Video'
})
</script>
<template>
  <div class="w-full h-full flex min-h-[100vh]">
    <div class="w-1/2">
      <GPSMap enable-altitude-manipulation />
    </div>
    <div class="w-1/2">
      <VideoStreaming />
    </div>
  </div>
</template>

<style lang="scss"></style>
