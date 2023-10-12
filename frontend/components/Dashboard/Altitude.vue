<script setup lang="ts">
import { Mountain } from 'lucide-vue-next'

const altitude = ref(103)
let interval: NodeJS.Timeout | null = null

onMounted(() => {
  interval = setInterval(() => {
    altitude.value = Math.floor(Math.random() * (104 - 98 + 1) + 98)
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
    <Mountain :size="32" class="mt-1" />
    <h3 class="text-xl text-primary font-bold">{{ altitude }} m</h3>
    <p class="text-sm">Altitude</p>
  </div>
</template>

<style scoped lang="scss"></style>
