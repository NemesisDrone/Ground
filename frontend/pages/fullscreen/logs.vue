<script setup lang="ts">
import LogsViewer from '~/components/Operations/Dashboard/LogsViewer.vue'
definePageMeta({
  layout: 'sidebar'
})
</script>

<template>
  <div class="h-[100vh]">
    <LogsViewer />
  </div>
</template>

<style scoped lang="scss"></style>
