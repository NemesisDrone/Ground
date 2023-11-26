<script setup lang="ts">
import { ScreenShare, Image } from 'lucide-vue-next'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  allowStyleChange: {
    type: Boolean,
    default: false
  },
  allowOpenInNewTab: {
    type: Boolean,
    default: false
  }
})

const imageViewerStyle = ref('cover')
const changeImageViewerStyle = () => {
  if (imageViewerStyle.value === 'cover') {
    imageViewerStyle.value = 'contain'
  } else {
    imageViewerStyle.value = 'cover'
  }
}

const imageViewerStyleComputed = computed(() => {
  return {
    'object-contain': imageViewerStyle.value === 'contain',
    'object-cover': imageViewerStyle.value === 'cover'
  }
})
</script>

<template>
  <div class="rounded-md bg-neutral-900 h-full p-2 relative">
    <img
      :src="src"
      class="h-full w-full"
      alt=""
      :class="imageViewerStyleComputed"
    />
    <button
      v-if="allowOpenInNewTab"
      class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
      title="Open in a new tab"
    >
      <ScreenShare :size="24" />
    </button>
    <button
      v-if="allowStyleChange"
      class="absolute top-0 left-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 ml-2.5 text-primary"
      title="Change image viewer style"
      @click="changeImageViewerStyle"
    >
      <Image :size="24" />
    </button>
  </div>
</template>

<style scoped lang="scss"></style>
