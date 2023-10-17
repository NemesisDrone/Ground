<script setup lang="ts">
import {
  BatteryFull,
  BatteryMedium,
  BatteryLow,
  Battery,
  BatteryWarning
} from 'lucide-vue-next'
import { getBatteryStatus } from '~/utils/sensors'
import { BatteryStatus } from '~/types/sensors.types'
import { storeToRefs } from 'pinia'
import { useSensorsStore } from '~/store/sensors'

const { battery } = storeToRefs(useSensorsStore())

const batteryStatus = computed(() => {
  return getBatteryStatus(battery.value)
})
</script>

<template>
  <div
    class="rounded bg-neutral-900 h-full flex flex-col items-center justify-center gap-0.5"
  >
    <BatteryFull
      v-if="batteryStatus === BatteryStatus.FULL"
      :size="32"
      class="mt-1 text-green-600"
    />
    <BatteryMedium
      v-else-if="batteryStatus === BatteryStatus.MEDIUM"
      :size="32"
      class="mt-1 text-green-900"
    />
    <BatteryLow
      v-else-if="batteryStatus === BatteryStatus.LOW"
      :size="32"
      class="mt-1 text-orange-500"
    />
    <BatteryWarning
      v-else-if="batteryStatus === BatteryStatus.VERY_LOW"
      :size="32"
      class="mt-1 text-red-600"
    />
    <Battery
      v-else-if="batteryStatus === BatteryStatus.EMPTY"
      :size="32"
      class="mt-1 text-red-900"
    />
    <h3
      class="text-xl font-bold"
      :class="{
        'text-red-900': batteryStatus === BatteryStatus.EMPTY,
        'text-red-600': batteryStatus === BatteryStatus.VERY_LOW,
        'text-orange-500': batteryStatus === BatteryStatus.LOW,
        'text-green-900': batteryStatus === BatteryStatus.MEDIUM,
        'text-green-600': batteryStatus === BatteryStatus.FULL
      }"
    >
      {{ battery }} %
    </h3>
    <p class="text-sm">Battery</p>
  </div>
</template>

<style scoped lang="scss"></style>
