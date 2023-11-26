<script setup lang="ts">
import LogsViewer from '~/components/Operations/LogsViewer.vue'
definePageMeta({
  // @ts-ignore
  layout: 'operations'
})
</script>

<template>
  <div class="h-[100vh]">
    <LogsViewer />
  </div>
</template>

<style scoped lang="scss"></style>
