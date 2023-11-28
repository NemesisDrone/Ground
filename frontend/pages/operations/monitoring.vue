<script lang="ts" setup>
import GPSMap from '~/components/Operations/GPSMap.vue'
import VideoStreaming from '~/components/Operations/VideoStreaming.vue'
import ImageViewer from '~/components/ui/image-viewer/ImageViewer.vue'
import ScrollArea from '~/components/ui/scroll-area/ScrollArea.vue'
import { CameraOff } from 'lucide-vue-next'
definePageMeta({
  layout: 'operations'
})
useHead({
  title: 'Monitoring'
})

const images = [
  {
    id: 1,
    src: '/images/demo/img1.jpg'
  },
  {
    id: 2,
    src: '/images/demo/img2.jpg'
  },
  {
    id: 3,
    src: '/images/demo/img3.jpg'
  },
  {
    id: 4,
    src: '/images/demo/img4.jpg'
  },
  {
    id: 5,
    src: '/images/demo/img3.jpg'
  },
  {
    id: 6,
    src: '/images/demo/img1.jpg'
  },
  {
    id: 7,
    src: '/images/demo/img4.jpg'
  },
  {
    id: 8,
    src: '/images/demo/img2.jpg'
  },
  {
    id: 9,
    src: '/images/demo/img3.jpg'
  }
]

const selectedImage = ref<any>(null)
const imageViewer = ref<any>(null)

const selectImage = (image: { id: number; src: string }) => {
  selectedImage.value = image
}

onMounted(() => {
  if (images.length > 0) {
    selectedImage.value = images[0]
  }
})
</script>
<template>
  <div class="w-full h-[100vh] p-4">
    <div class="h-1/2 w-full flex gap-4">
      <div class="w-1/2 h-full">
        <ImageViewer
          :src="selectedImage ? selectedImage.src : ''"
          :allow-style-change="true"
          :allow-zoom="true"
        />
      </div>
      <div class="w-1/2 h-full">
        <div class="rounded-md bg-neutral-900 h-full p-2">
          <VideoStreaming />
        </div>
      </div>
    </div>
    <div class="h-1/2 w-full flex gap-4 pt-4">
      <scroll-area :scroll-to-bottom="false" class="w-2/3 h-full">
        <div
          class="h-full grid grid-cols-4 gap-2 rounded-md bg-neutral-900 p-2"
        >
          <div
            v-for="img in images"
            :key="img.id"
            class="rounded-md border-4 h-[calc(25vh-2rem)] cursor-pointer"
            :class="{
              'border-primary':
                img.id === (selectedImage ? selectedImage.id : -1)
            }"
            @click="selectImage(img)"
          >
            <img
              :src="img.src"
              alt=""
              class="h-full w-full rounded-[0.12rem]"
            />
          </div>
          <div
            v-if="images.length < 8"
            v-for="i in 8 - images.length"
            :key="i"
          >
            <div
              class="rounded-md border-4 h-[calc(25vh-2rem)] flex justify-center items-center"
            >
              <CameraOff :size="32" color="#27272A" />
            </div>
          </div>
        </div>
      </scroll-area>
      <div class="w-1/3 h-full"></div>
    </div>
  </div>
</template>

<style lang="scss"></style>
