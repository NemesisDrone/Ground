<script setup lang="ts">
import { ScreenShare, Image, Fullscreen } from 'lucide-vue-next'

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

    const localScale = scale.value - event.deltaY * 0.001
    scale.value = Math.min(Math.max(1, localScale), 4)

    originX.value = event.clientX - image.value.offsetLeft
    originY.value = event.clientY - image.value.offsetTop
  }
}

const imageStyleComputed = computed(() => {
  return {
    transform: `scale(${scale.value})`,
    transformOrigin: `${originX.value}px ${originY.value}px`
  }
})

const setDefaultImageStyle = () => {
  scale.value = 1
}

const selectionBox = ref<HTMLElement | null>(null)
const isSelecting = ref(false)
const selection = reactive({
  startX: 0,
  startY: 0,
  endX: 0,
  endY: 0,
  left: 0,
  top: 0,
  width: 0,
  height: 0
})
const startSelection = (event: MouseEvent) => {
  if (event.buttons != 1 || imageContainer.value == null) return
  isSelecting.value = true

  selection.startX =
    event.clientX - imageContainer.value.getBoundingClientRect().left
  selection.startY =
    event.clientY - imageContainer.value.getBoundingClientRect().top
  selection.width = 0
  selection.height = 0
  selection.endX = 0
  selection.endY = 0
}

const updateSelection = (event: MouseEvent) => {
  if (
    !isSelecting.value ||
    event.buttons != 1 ||
    imageContainer.value == null
  )
    return

  selection.endX =
    event.clientX - imageContainer.value?.getBoundingClientRect().left
  selection.endY =
    event.clientY - imageContainer.value?.getBoundingClientRect().top

  const x = Math.min(selection.startX, selection.endX)
  const y = Math.min(selection.startY, selection.endY)
  const width = Math.abs(selection.endX - selection.startX)
  const height = Math.abs(selection.endY - selection.startY)

  selection.left = x
  selection.top = y
  selection.width = width
  selection.height = height
}

const endSelection = (event: MouseEvent) => {
  if (
    !image.value ||
    event.buttons != 0 ||
    !isSelecting.value ||
    !imageContainer.value
  )
    return
  isSelecting.value = false

  const scaleWidth =
    imageContainer.value.clientWidth /
    Math.abs(selection.endX - selection.startX)
  const scaleHeight =
    imageContainer.value.clientHeight /
    Math.abs(selection.endY - selection.startY)

  scale.value = Math.max(scaleWidth, scaleHeight)
  const x = selection.startX
  const y = selection.endY

  originX.value = x
  originY.value = y

  selection.left = 0
  selection.top = 0
  selection.width = 0
  selection.height = 0
}

const selectionBoxStyleComputed = computed(() => {
  return {
    left: `${selection.left}px`,
    top: `${selection.top}px`,
    width: `${selection.width}px`,
    height: `${selection.height}px`
  }
})
</script>

<template>
  <div
    class="rounded-md bg-neutral-900 h-full p-2 relative overflow-hidden select-text"
    ref="imageContainer"
    @wheel="onWheelEvent"
    @mousedown="startSelection"
    @mouseup="endSelection"
    @mousemove="updateSelection"
  >
    <img
      :src="src"
      ref="image"
      class="h-full w-full"
      :style="imageStyleComputed"
      alt=""
      :class="imageViewerStyleComputed"
      draggable="false"
    />
    <div
      class="selection-box"
      ref="selectionBox"
      :style="selectionBoxStyleComputed"
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
