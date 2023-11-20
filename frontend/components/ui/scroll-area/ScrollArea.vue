<script setup lang="ts">
import {
  ScrollAreaCorner,
  ScrollAreaRoot,
  type ScrollAreaRootProps,
  ScrollAreaViewport
} from 'radix-vue'
import ScrollBar from './ScrollBar.vue'
import { cn } from '@/helpers/utils'

const props = withDefaults(
  defineProps<
    ScrollAreaRootProps & { class?: string; scrollToBottom: boolean }
  >(),
  {
    class: '',
    orientation: 'vertical',
    scrollToBottom: false
  }
)
const intervalScrollToBottom = ref<NodeJS.Timeout | null>(null)
const isScrolling = ref(false)

onMounted(() => {
  if (props.scrollToBottom) {
    intervalScrollToBottom.value = setInterval(() => {
      if (!props.scrollToBottom) return
      const scrollArea = document.querySelector(
        '.radix-scroll-area'
      ) as HTMLElement
      if (!scrollArea) {
        return
      }
      scrollArea.scrollTop = scrollArea.scrollHeight
    }, 100)
  }
})

onUnmounted(() => {
  if (intervalScrollToBottom.value) {
    clearInterval(intervalScrollToBottom.value)
  }
})
</script>

<template>
  <ScrollAreaRoot
    :type="type"
    :class="cn('relative overflow-hidden', props.class)"
  >
    <ScrollAreaViewport
      class="h-full w-full rounded-[inherit] radix-scroll-area"
    >
      <slot />
    </ScrollAreaViewport>
    <ScrollBar />
    <ScrollAreaCorner />
  </ScrollAreaRoot>
</template>
