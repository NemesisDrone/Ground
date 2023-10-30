<script setup lang="ts">
import { Rabbit, CircleOff, Snail, Turtle } from 'lucide-vue-next'
import { PropulsorSpeedStatus } from '~/types/sensors.types'
import { getPropulsorSpeedStatus } from '~/helpers/sensors'
import { storeToRefs } from 'pinia'
import { useComponentsStore } from '~/store/components'

// const propulsorSpeed = ref(0)
const { propulsionController } = storeToRefs(useComponentsStore())
// let interval: NodeJS.Timeout | null = null
//
// onMounted(() => {
//   interval = setInterval(() => {
//     let speed = propulsorSpeed.value + 1
//     propulsorSpeed.value = speed <= 100 ? speed : 0
//   }, 150)
// })
//
const propulsorSpeedStatus = computed(() => {
  return getPropulsorSpeedStatus(propulsionController.value.speed)
})
//
// onUnmounted(() => {
//   if (interval) clearInterval(interval)
// })
</script>

<template>
  <div
    class="rounded bg-neutral-900 h-full flex flex-col items-center justify-center gap-0.5"
  >
    <Rabbit
      v-if="propulsorSpeedStatus === PropulsorSpeedStatus.HIGH"
      :size="32"
      class="mt-1"
    />
    <Turtle
      v-else-if="propulsorSpeedStatus === PropulsorSpeedStatus.MEDIUM"
      :size="32"
      class="mt-1"
    />
    <Snail
      v-else-if="propulsorSpeedStatus === PropulsorSpeedStatus.LOW"
      :size="32"
      class="mt-1"
    />
    <CircleOff
      v-else-if="propulsorSpeedStatus === PropulsorSpeedStatus.STOPPED"
      :size="32"
      class="mt-1 text-red-400"
    />
    <h3 class="text-xl text-primary font-bold">
      {{ propulsionController.speed }} %
    </h3>
    <p class="text-sm">Propulsor speed</p>
  </div>
</template>

<style scoped lang="scss"></style>
