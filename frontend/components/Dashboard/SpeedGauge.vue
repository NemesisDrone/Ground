<script setup lang="ts">
import { Gauge } from 'lucide-vue-next'
import { storeToRefs } from 'pinia'
import { useSensorsStore } from '~/store/sensors'

const { speed } = storeToRefs(useSensorsStore())
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
