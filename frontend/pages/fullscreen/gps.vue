<script setup lang="ts">
import GPSMap from '~/components/Operations/GPSMap.vue'
definePageMeta({
  // @ts-ignore
  layout: 'operations'
})
</script>

<template>
  <div class="h-[100vh]">
    <GPSMap />
  </div>
</template>

<style scoped lang="scss"></style>
