<script lang="ts" setup>
import GPSMap from '~/components/Operations/GPSMap.vue'
import VideoStreaming from '~/components/Operations/VideoStreaming.vue'
import ImageViewer from '~/components/ui/image-viewer/ImageViewer.vue'
definePageMeta({
  layout: 'operations'
})
useHead({
  title: 'Monitoring'
})
</script>
<template>
  <div class="w-full h-full min-h-[100vh]">
    <div class="h-1/2 w-full flex gap-4">
      <div class="w-1/2 h-full">
        <ImageViewer
          src="/images/demo/img1.jpg"
          class="mt-4 ml-4"
          :allow-style-change="true"
          :allow-zoom="true"
        />
      </div>
      <div class="w-1/2 h-full">
        <div class="rounded-md bg-neutral-900 h-full p-2 mt-4 mr-4">
          <VideoStreaming />
        </div>
      </div>
    </div>
    <div class="h-1/2 w-full flex">
      <div class="w-1/2 h-full"></div>
      <div class="w-1/2 h-full"></div>
    </div>
  </div>
</template>

<style lang="scss"></style>
