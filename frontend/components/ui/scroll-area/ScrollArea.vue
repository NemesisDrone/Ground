<script setup lang="ts">
import {
  ScrollAreaCorner,
  ScrollAreaRoot,
  type ScrollAreaRootProps,
  ScrollAreaViewport
} from 'radix-vue'
import ScrollBar from './ScrollBar.vue'
import { cn } from '@/helpers/utils'
import { Mouse, ScrollText } from 'lucide-vue-next'

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
      if (isScrolling.value) return
      const scrollArea = document.querySelector(
        '.radix-scroll-area'
      ) as HTMLElement
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
      <button
        v-if="scrollToBottom"
        class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="isScrolling = !isScrolling"
      >
        <ScrollText v-show="isScrolling" :size="24" />
        <Mouse v-show="!isScrolling" :size="24" />
      </button>
      <slot />
    </ScrollAreaViewport>
    <ScrollBar />
    <ScrollAreaCorner />
  </ScrollAreaRoot>
</template>
