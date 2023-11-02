<script setup lang="ts">
import {
  ScreenShare,
  XCircle,
  LocateFixed,
  LocateOff,
  ScanSearch
} from 'lucide-vue-next'
import { useSensorsStore } from '~/store/sensors'
import { storeToRefs } from 'pinia'
import { v4 as uuidv4 } from 'uuid'

const sensorsStore = useSensorsStore()
const { gpsPosition } = storeToRefs(sensorsStore)

const uniqueMapId = uuidv4()

const mapRef = useMapboxRef('map-gps-' + uniqueMapId)
const markerRef = useMapboxMarkerRef('marker')
const route = useRoute()

/**
 * Load the map after 1.5s
 */
const loadMap = ref(false)
onMounted(() => {
  setTimeout(() => {
    loadMap.value = true
  }, 1500)
})

const openInNewTab = () => {
  window.open('/fullscreen/gps', '_blank')
}
const closeWindow = () => {
  window.close()
}

const viewAttachedToDronePosition = ref(true)
watch(gpsPosition, () => {
  if (!mapRef.value || !markerRef.value) return

  if (viewAttachedToDronePosition.value) {
    mapRef.value?.panTo([gpsPosition.value.lat, gpsPosition.value.lng], {
      duration: 1000
    })
  }
  markerRef.value?.setLngLat([
    gpsPosition.value.lat,
    gpsPosition.value.lng
  ])
})

const goToInitialZoom = () => {
  if (!mapRef.value) return

  mapRef.value?.zoomTo(15.5)
}
</script>
<template>
  <div class="relative h-full m-0 p-0 overflow-hidden">
    <MapboxMap
      v-if="loadMap"
      :map-id="`map-gps-${uniqueMapId}`"
      :options="{
        style: 'mapbox://styles/mapbox/satellite-streets-v12', // style URL
        // style: 'mapbox://styles/mapbox/dark-v11',
        // pitch: 60,
        // center: [gpsPosition.lat, gpsPosition.lng], // starting position
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
        title="Open in new tab"
      >
        <ScreenShare :size="24" />
      </button>
      <button
        class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        v-else
        @click="closeWindow"
        title="Close window"
      >
        <XCircle :size="24" />
      </button>
      <button
        class="absolute top-10 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="viewAttachedToDronePosition = !viewAttachedToDronePosition"
        :title="viewAttachedToDronePosition ? 'Detach' : 'Attach'"
      >
        <LocateOff v-if="viewAttachedToDronePosition" :size="24" />
        <LocateFixed v-else :size="24" />
      </button>
      <button
        class="absolute top-20 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="goToInitialZoom"
        title="Go to initial zoom"
      >
        <ScanSearch :size="24" />
      </button>
    </MapboxMap>
  </div>
</template>
