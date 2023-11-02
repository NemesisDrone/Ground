<script lang="ts" setup>
import GPSMap from '~/components/Dashboard/GPSMap.vue'
import VideoStreaming from '~/components/Dashboard/VideoStreaming.vue'
definePageMeta({
  layout: 'dashboard'
})
</script>
<template>
  <div class="w-full h-full flex min-h-[100vh]">
    <div class="w-1/2">
      <GPSMap />
    </div>
    <div class="w-1/2">
      <VideoStreaming />
    </div>
  </div>
</template>

<style lang="scss"></style>
