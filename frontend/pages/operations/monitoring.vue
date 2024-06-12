<script lang="ts" setup>
import VideoStreaming from '~/components/Operations/Dashboard/VideoStreaming.vue'
import {
  CameraOff,
  MousePointerSquare,
  XCircle,
  Download
} from 'lucide-vue-next'
import { useMonitoringStore } from '~/store/monitoring'
import { DroneImage } from '~/types/images.types'
definePageMeta({
  layout: 'sidebar'
})
useHead({
  title: 'Monitoring'
})

const monitoringStore = useMonitoringStore()

const selectedImage = ref<DroneImage | null>(null)
const isImagesLoading = ref(false)
const isImageDeletionLoading = ref(false)

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

const deleteImage = async (image: DroneImage) => {
  isImageDeletionLoading.value = true

  await monitoringStore.deleteImage(image)
  if (selectedImage.value?.id === image.id) {
    if (monitoringStore.images.length > 0) {
      selectedImage.value = monitoringStore.images[0]
    } else {
      selectedImage.value = null
    }
  }

  isImageDeletionLoading.value = false
}

const downloadImage = async (image: DroneImage) => {
  const link = document.createElement('a')
  link.href = image.url
  link.target = '_blank'
  link.download = image.url.split('/').pop() || ''
  link.click()
}
</script>
<template>
  <div class="w-full h-[100vh] p-4">
    <div class="h-1/2 w-full flex gap-4">
      <div class="w-1/2 h-full">
        <UiOverlay :show="isImagesLoading">
          <UiImageViewer
            :src="selectedImage ? selectedImage.url : ''"
            :allow-style-change="true"
            :allow-zoom="true"
            :allow-open-in-new-tab="true"
          />
        </UiOverlay>
      </div>
      <div class="w-1/2 h-full">
        <div class="rounded-md bg-neutral-900 h-full p-2">
          <VideoStreaming />
        </div>
      </div>
    </div>
    <div class="h-1/2 w-full flex gap-4 pt-4">
      <UiScrollArea class="w-5/6 h-full" :scroll-to-bottom="false">
        <UiOverlay :show="isImagesLoading">
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
              <UiDialog>
                <UiContextMenu>
                  <UiContextMenuTrigger>
                    <img
                      :src="img.url"
                      alt=""
                      class="h-full w-full rounded-[0.12rem] object-cover"
                    />
                  </UiContextMenuTrigger>
                  <UiContextMenuContent>
                    <UiContextMenuItem
                      @click="selectImage(img)"
                      :disabled="selectedImage?.id === img.id"
                    >
                      <MousePointerSquare :size="18" class="mr-2" />
                      Select
                    </UiContextMenuItem>
                    <UiContextMenuItem @click="downloadImage(img)">
                      <Download :size="18" class="mr-2" />
                      Download
                    </UiContextMenuItem>
                    <UiDialogTrigger asChild>
                      <UiContextMenuItem class="text-red-500">
                        <XCircle :size="18" class="mr-2" />
                        Delete
                      </UiContextMenuItem>
                    </UiDialogTrigger>
                  </UiContextMenuContent>
                </UiContextMenu>
                <UiDialogContent>
                  <UiDialogHeader>
                    <UiDialogTitle>Delete picture?</UiDialogTitle>
                    <UiDialogDescription>
                      The picture will be deleted permanently.
                    </UiDialogDescription>
                  </UiDialogHeader>
                  <UiDialogFooter>
                    <UiButton
                      variant="destructive"
                      @click="deleteImage(img)"
                      :is-loading="isImageDeletionLoading"
                    >
                      Confirm
                    </UiButton>
                  </UiDialogFooter>
                </UiDialogContent>
              </UiDialog>
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
        </UiOverlay>
      </UiScrollArea>
      <div class="w-1/6 h-full">
        <UiButton class="w-full" @click="monitoringStore.takePicture()">
          <CameraOff :size="24" color="#27272A" class="mr-2" />
          Take Picture
        </UiButton>
      </div>
    </div>
  </div>
</template>

<style lang="scss"></style>
