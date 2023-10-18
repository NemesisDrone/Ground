<script setup lang="ts">
import LogsViewer from '~/components/Dashboard/LogsViewer.vue'
definePageMeta({
  // @ts-ignore
  layout: 'dashboard'
})
</script>

<template>
  <div class="h-[100vh]">
    <LogsViewer />
  </div>
</template>

<style scoped lang="scss"></style>
