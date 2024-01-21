<script setup lang="ts">
import { PlayCircle } from 'lucide-vue-next'
</script>

<template>
  <div class="rounded bg-neutral-900 h-full p-4 flex flex-col">
    <h4>Session recorder</h4>
    <div class="flex mt-2 justify-between items-center">
      <UiButton>
        <span class="flex items-center gap-2">
          <PlayCircle :size="20" />
          <span>Start</span>
        </span>
      </UiButton>
      <div>
        <span class="text-red-600">Currently not recording</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss"></style>
