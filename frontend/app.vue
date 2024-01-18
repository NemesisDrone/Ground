<script setup lang="ts">
useHead({
  bodyAttrs: {
    class: 'bg-background dark'
  }
})

import Toaster from '@/components/ui/toast/Toaster.vue'
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  <Toaster />
</template>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.4s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
