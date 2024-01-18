<script setup lang="ts">
const { show } = defineProps<{
  show: boolean
}>()
</script>

<template>
  <div class="h-full w-full relative">
    <transition name="overlay">
      <div
        v-if="show"
        class="bg-black opacity-70 z-50 absolute flex items-center justify-center w-full h-full"
      >
        <div
          class="left-4 inline-block h-7 w-7 animate-spin rounded-full border-primary border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
          role="status"
        ></div>
      </div>
    </transition>
    <slot />
  </div>
</template>

<style scoped lang="scss">
.overlay-enter-active,
.overlay-leave-active {
  transition: all 0.4s;
}
.overlay-enter-from,
.overlay-leave-to {
  opacity: 0;
}
</style>
