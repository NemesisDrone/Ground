<script lang="ts" setup>
import VideoStreaming from '~/components/Operations/VideoStreaming.vue'
import ImageViewer from '~/components/ui/image-viewer/ImageViewer.vue'
import ScrollArea from '~/components/ui/scroll-area/ScrollArea.vue'
import { CameraOff, MousePointerSquare, XCircle } from 'lucide-vue-next'
import { useMonitoringStore } from '~/store/monitoring'
import { DroneImage } from '~/types/images.types'
import Overlay from '~/components/ui/overlay/Overlay.vue'
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger
} from '@/components/ui/context-menu'
definePageMeta({
  layout: 'sidebar'
})
useHead({
  title: 'Monitoring'
})

const monitoringStore = useMonitoringStore()

const selectedImage = ref<DroneImage | null>(null)
const isImagesLoading = ref(false)

const selectImage = (image: DroneImage) => {
  selectedImage.value = image
}

onMounted(async () => {
  isImagesLoading.value = true
  await monitoringStore.getImages()
  isImagesLoading.value = false

  if (monitoringStore.images.length > 0) {
    selectedImage.value = monitoringStore.images[0]
  }
})
</script>
<template>
  <div class="w-full h-[100vh] p-4">
    <div class="h-1/2 w-full flex gap-4">
      <div class="w-1/2 h-full">
        <Overlay :show="isImagesLoading">
          <ImageViewer
            :src="selectedImage ? selectedImage.url : ''"
            :allow-style-change="true"
            :allow-zoom="true"
            :allow-open-in-new-tab="true"
          />
        </Overlay>
      </div>
      <div class="w-1/2 h-full">
        <div class="rounded-md bg-neutral-900 h-full p-2">
          <VideoStreaming />
        </div>
      </div>
    </div>
    <div class="h-1/2 w-full flex gap-4 pt-4">
      <scroll-area class="w-2/3 h-full" :scroll-to-bottom="false">
        <Overlay :show="isImagesLoading">
          <div
            class="h-full grid grid-cols-4 gap-2 rounded-md bg-neutral-900 p-2"
          >
            <div
              v-for="img in monitoringStore.images"
              :key="img.id"
              class="rounded-md border-4 h-[calc(25vh-2rem)] cursor-pointer"
              :class="{
                'border-primary':
                  img.id === (selectedImage ? selectedImage.id : -1)
              }"
              @click="selectImage(img)"
            >
              <ContextMenu>
                <ContextMenuTrigger>
                  <img
                    :src="img.url"
                    alt=""
                    class="h-full w-full rounded-[0.12rem]"
                  />
                </ContextMenuTrigger>
                <ContextMenuContent>
                  <ContextMenuItem @click="selectImage(img)">
                    <MousePointerSquare :size="22" class="mr-2" />
                    Select
                  </ContextMenuItem>
                  <ContextMenuItem class="text-red-500">
                    <XCircle :size="22" class="mr-2" />
                    Delete
                  </ContextMenuItem>
                </ContextMenuContent>
              </ContextMenu>
            </div>
            <div
              v-if="monitoringStore.images.length < 8"
              v-for="i in 8 - monitoringStore.images.length"
              :key="i"
            >
              <div
                class="rounded-md border-4 h-[calc(25vh-2rem)] flex justify-center items-center"
              >
                <CameraOff :size="32" color="#27272A" />
              </div>
            </div>
          </div>
        </Overlay>
      </scroll-area>
      <div class="w-1/3 h-full"></div>
    </div>
  </div>
</template>

<style lang="scss"></style>
