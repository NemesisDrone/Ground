# Frontend documentation

Here is some nice documentations to read : 
- [Vuejs 3](https://vuejs.org/)
- [Nuxt](https://nuxtjs.org/)
- [Typescript](https://www.typescriptlang.org/)
- [Tailwindcss](https://tailwindcss.com/)
- [How JWT works](https://sureshdsk.dev/how-json-web-token-jwt-authentication-works/)

## Add a custom dashboard layout
To add a custom dashboard layout, you need to create a new page in `pages/dashboard` and add the following code : 
```vue
<script lang="ts" setup>
import GPSMap from '~/components/Dashboard/GPSMap.vue'
import VideoStreaming from '~/components/Dashboard/VideoStreaming.vue'
definePageMeta({
  layout: 'dashboard'
})
</script>
<template>
  <div class="w-full h-full flex min-h-[100vh]">
    <div class="w-1/2">
      <GPSMap />
    </div>
    <div class="w-1/2">
      <VideoStreaming />
    </div>
  </div>
</template>

<style lang="scss"></style>
```
Then, you need to add the new page to the navigation in the `layouts/dashboard.vue` file, inside the dashboardLayouts list :
```ts
const dashboardLayouts = [
  ...
  {
    icon: KanbanSquare, // Choose an icon from Lucide icons,
    title: 'The name of the layout',
    route: '/dashboard/the-url-of-the-page'
  },
  ...
]
```
