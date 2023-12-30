<script setup lang="ts">
import { ScreenShare, Fullscreen, CameraOff, Image } from 'lucide-vue-next'

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
  },
  allowZoom: {
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

const image = ref<HTMLElement | null>(null)
const imageContainer = ref<HTMLElement | null>(null)
const scale = ref(1)
const originX = ref(0)
const originY = ref(0)

const onWheelEvent = (event: WheelEvent) => {
  event.preventDefault()
  if (image.value && props.allowZoom && imageContainer.value) {
    const mouseX =
      event.clientX - imageContainer.value.getBoundingClientRect().left
    const mouseY =
      event.clientY - imageContainer.value.getBoundingClientRect().top

    const localScale = scale.value - event.deltaY * 0.005
    scale.value = Math.min(Math.max(1, localScale), 25)

    const newX = event.clientX - image.value.offsetLeft
    const newY = event.clientY - image.value.offsetTop

    const deltaX = mouseX - newX
    const deltaY = mouseY - newY
    console.log(deltaX, deltaY)

    originX.value = newX
    originY.value = newY
  }
}

const imageStyleComputed = computed(() => {
  return {
    transform: `scale(${scale.value})`,
    transformOrigin: `${originX.value}px ${originY.value}px`
  }
})

const hasImageToMove = ref(false)
const onMouseDown = (event: MouseEvent) => {
  if (event.button !== 0) return
  hasImageToMove.value = true
}

const onMouseMove = (event: MouseEvent) => {
  if (event.button !== 0) return
  if (hasImageToMove.value && image.value && imageContainer.value) {
    const mouseX =
      event.clientX - imageContainer.value.getBoundingClientRect().left
    const mouseY =
      event.clientY - imageContainer.value.getBoundingClientRect().top
    originX.value = mouseX
    originY.value = mouseY
  }
}

const onMouseUp = (event: MouseEvent) => {
  if (event.button !== 0) return
  hasImageToMove.value = false
}

const setDefaultImageStyle = () => {
  scale.value = 1
}

watch(
  () => props.src,
  () => {
    setDefaultImageStyle()
  }
)

const openInNewTab = () => {
  window.open(`/fullscreen/${btoa(props.src)}/viewer`, '_blank')
}
</script>

<template>
  <div
    class="rounded-md bg-neutral-900 h-full p-2 relative overflow-hidden select-text"
    ref="imageContainer"
    @wheel="onWheelEvent"
  >
    <img
      v-if="src"
      :src="src"
      ref="image"
      class="h-full w-full"
      :style="imageStyleComputed"
      alt=""
      :class="imageViewerStyleComputed"
      draggable="false"
      @mousedown="onMouseDown"
      @mouseup="onMouseUp"
      @mousemove="onMouseMove"
    />
    <div v-else class="h-full w-full flex items-center justify-center">
      <CameraOff :size="72" color="#27272A" />
    </div>
    <button
      v-if="allowOpenInNewTab"
      class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
      title="Open in a new tab"
      @click="openInNewTab"
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
    <button
      v-if="allowZoom"
      class="absolute top-10 left-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 ml-2.5 text-primary"
      title="Return to default image zoom"
      @click="setDefaultImageStyle"
    >
      <Fullscreen :size="24" />
    </button>
  </div>
</template>

<style scoped lang="scss">
.selection-box {
  border: 2px dashed #131110;
  position: absolute;
  background-color: rgba(0, 0, 0, 0.5);
  pointer-events: none;
}
</style>
