<script setup lang="ts">
import { Gauge } from 'lucide-vue-next'

const speed = ref(27)
let interval: NodeJS.Timeout | null = null

onMounted(() => {
  interval = setInterval(() => {
    speed.value = Math.floor(Math.random() * (30 - 25 + 1) + 25)
  }, 1000)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<template>
  <div
    class="rounded bg-neutral-900 h-full flex flex-col items-center justify-center gap-0.5"
  >
    <Gauge :size="32" class="mt-1" />
    <h3 class="text-xl text-primary font-bold">{{ speed }} km/h</h3>
    <p class="text-sm">Speed</p>
  </div>
</template>

<style scoped lang="scss"></style>
