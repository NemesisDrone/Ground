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

      <button
        class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        v-if="route.path !== '/fullscreen/gps'"
        @click="openInNewTab"
      >
        <ScreenShare :size="24" />
      </button>
      <button
        class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        v-else
        @click="closeWindow"
      >
        <XCircle :size="32" />
      </button>
    </MapboxMap>
  </div>
</template>
