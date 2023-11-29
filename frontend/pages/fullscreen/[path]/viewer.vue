<script setup lang="ts">
import ImageViewer from '~/components/ui/image-viewer/ImageViewer.vue'
const route = useRoute()

const src = atob(route.params.path)
console.log(src)
</script>

<template>
  <div class="h-[100vh]">
    <ImageViewer
      :src="src"
      :allow-style-change="true"
      :allow-zoom="true"
    />
  </div>
</template>

<style scoped lang="scss"></style>
