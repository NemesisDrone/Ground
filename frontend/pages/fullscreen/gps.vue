<script setup lang="ts">
import GPSMap from '~/components/Operations/Dashboard/GPSMap.vue'

definePageMeta({
  layout: 'sidebar'
})
</script>

<template>
  <div class="h-[100vh]">
    <GPSMap enable-altitude-manipulation />
  </div>
</template>

<style scoped lang="scss"></style>
