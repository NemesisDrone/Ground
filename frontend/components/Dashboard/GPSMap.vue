<script setup lang="ts">
import { ScreenShare, XCircle } from 'lucide-vue-next'

const mapRef = useMapboxRef('map-gps')
const route = useRoute()

const openInNewTab = () => {
  window.open('/fullscreen/gps', '_blank')
}

const closeWindow = () => {
  window.close()
}
</script>
<template>
  <div class="relative h-full m-0 p-0 overflow-hidden">
    <MapboxMap
      map-id="map-gps"
      :options="{
        style: 'mapbox://styles/mapbox/satellite-streets-v12', // style URL
        // style: 'mapbox://styles/mapbox/dark-v11',
        // pitch: 60,
        center: [-0.7563779, 48.0879123], // starting position
        zoom: 15.5 // starting zoom
      }"
    >
      <MapboxDefaultMarker
        marker-id="marker"
        :lnglat="[-0.7563779, 48.0879123]"
      />

      <ScreenShare
        v-if="route.path !== '/fullscreen/gps'"
        class="absolute top-0 right-0 m-2 cursor-pointer"
        color="black"
        :size="24"
        @click="openInNewTab"
      />
      <XCircle
        v-else
        class="absolute top-0 right-0 m-3 cursor-pointer"
        color="black"
        :size="32"
        @click="closeWindow"
      />
    </MapboxMap>
  </div>
</template>
