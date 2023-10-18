<script setup lang="ts">
import { ScreenShare, XCircle } from 'lucide-vue-next'
import { useSensorsStore } from '~/store/sensors'
import { storeToRefs } from 'pinia'

const sensorsStore = useSensorsStore()
const { gpsPosition } = storeToRefs(sensorsStore)

const mapRef = useMapboxRef('map-gps')
const route = useRoute()

const loadMap = ref(false)

const openInNewTab = () => {
  window.open('/fullscreen/gps', '_blank')
}

const closeWindow = () => {
  window.close()
}

onMounted(() => {
  setTimeout(() => {
    loadMap.value = true
  }, 1500)
})
</script>
<template>
  <div class="relative h-full m-0 p-0 overflow-hidden">
    <MapboxMap
      v-if="loadMap"
      map-id="map-gps"
      :options="{
        style: 'mapbox://styles/mapbox/satellite-streets-v12', // style URL
        // style: 'mapbox://styles/mapbox/dark-v11',
        // pitch: 60,
        center: [gpsPosition.lat, gpsPosition.lng], // starting position
        zoom: 15.5 // starting zoom
      }"
    >
      <MapboxDefaultMarker
        marker-id="marker"
        :lnglat="[gpsPosition.lat, gpsPosition.lng]"
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
