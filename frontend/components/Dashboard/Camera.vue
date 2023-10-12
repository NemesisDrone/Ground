<script setup lang="ts">
import { Video } from 'lucide-vue-next'
</script>

<template>
  <div
    class="rounded bg-neutral-900 h-full flex flex-col items-center justify-center gap-0.5"
  >
    <Video :size="32" class="mt-1" />
    <h3 class="text-xl text-primary font-bold">2</h3>
    <p class="text-sm">Other</p>
  </div>
</template>

<style scoped lang="scss"></style>
