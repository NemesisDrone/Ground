<script setup lang="ts">
import {
  ScreenShare,
  XCircle,
  LocateFixed,
  LocateOff,
  ScanSearch,
  Box,
  Map
} from 'lucide-vue-next'
import { useSensorsStore } from '~/store/sensors'
import { storeToRefs } from 'pinia'
import { v4 as uuidv4 } from 'uuid'
import * as THREE from 'three'
import {
  getMapBox3DDroneModelLayer,
  getMapBoxDroneDirectionLineLayer
} from '~/helpers/mapBoxLayers'
import { MathUtils } from 'three'

const sensorsStore = useSensorsStore()
const { gpsPosition } = storeToRefs(sensorsStore)

const uniqueMapId = uuidv4()

const mapRef = useMapboxRef('map-gps-' + uniqueMapId)
const route = useRoute()

/**
 * Load the map after 1.5s
 */
const loadMap = ref(false)
onMounted(() => {
  setTimeout(() => {
    loadMap.value = true
    // Set default center to esiea position
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
  if (!mapRef.value) return
  console.log(gpsPosition.value)
  if (viewAttachedToDronePosition.value) {
    mapRef.value?.panTo([gpsPosition.value.lat, gpsPosition.value.lng], {
      duration: 1000
    })
  }
})

const toggleAttachedView = () => {
  viewAttachedToDronePosition.value = !viewAttachedToDronePosition.value
  if (viewAttachedToDronePosition.value) {
    mapRef.value?.panTo([gpsPosition.value.lat, gpsPosition.value.lng], {
      duration: 1000
    })
  }
}

const add3dBuildings = () => {
  const layers = mapRef.value?.getStyle().layers
  // @ts-ignore
  const labelLayerId = layers.find(
    // @ts-ignore
    (layer) => layer.type === 'symbol' && layer.layout['text-field']
  ).id

  mapRef.value?.addLayer(
    {
      id: 'add-3d-buildings',
      source: 'composite',
      'source-layer': 'building',
      filter: ['==', 'extrude', 'true'],
      type: 'fill-extrusion',
      minzoom: 15,
      paint: {
        'fill-extrusion-color': '#aaa',

        'fill-extrusion-height': [
          'interpolate',
          ['linear'],
          ['zoom'],
          15,
          0,
          15.05,
          ['get', 'height']
        ],
        'fill-extrusion-base': [
          'interpolate',
          ['linear'],
          ['zoom'],
          15,
          0,
          15.05,
          ['get', 'min_height']
        ],
        'fill-extrusion-opacity': 0.6
      }
    },
    labelLayerId
  )
}

const use3dBuildings = ref(true)
const toggle3dBuildings = () => {
  if (!mapRef.value) return
  use3dBuildings.value = !use3dBuildings.value

  if (use3dBuildings.value) {
    add3dBuildings()
  } else {
    mapRef.value?.removeLayer('add-3d-buildings')
  }
}

const useSatteliteView = ref(true)

const toggleMapView = () => {
  if (!mapRef.value) return
  useSatteliteView.value = !useSatteliteView.value

  if (useSatteliteView.value) {
    mapRef.value?.setStyle('mapbox://styles/mapbox/satellite-streets-v12')
  } else {
    mapRef.value?.setStyle('mapbox://styles/mapbox/dark-v11')
  }
}

let scene: THREE.Scene | null = null
let camera: THREE.Camera | null = null

watch(mapRef, () => {
  if (!mapRef.value) return
  mapRef.value.setCenter([gpsPosition.value.lat, gpsPosition.value.lng])
  mapRef.value.on('style.load', () => {
    if (use3dBuildings.value) add3dBuildings()
  })

  const layerDrone = getMapBox3DDroneModelLayer(
    camera,
    scene,
    mapRef.value
  )

  mapRef.value?.on('style.load', () => {
    const distance =
      0.00015 * (Math.pow(2, 22 - (mapRef.value?.getZoom() || 0)) / 8)
    const yaw = MathUtils.degToRad(sensorsStore.full.yaw)
    const lat = gpsPosition.value.lat
    const lng = gpsPosition.value.lng

    const newLng = lng + distance * Math.cos(yaw)
    const newLat = lat + distance * Math.sin(yaw)

    mapRef.value?.addSource('droneDirection', {
      type: 'geojson',
      data: {
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'LineString',
          coordinates: [
            // Position of the drone
            [gpsPosition.value.lat, gpsPosition.value.lng],
            // Position of the direction last point of the drone
            [newLat, newLng]
          ]
        }
      }
    })
    mapRef.value?.addLayer(
      {
        id: 'droneDirection',
        type: 'line',
        source: 'droneDirection',
        layout: {
          'line-join': 'round',
          'line-cap': 'round'
        },
        paint: {
          'line-color': '#FF0000',
          'line-width': 6
        }
      },
      'waterway-label'
    )
    mapRef.value?.addLayer(layerDrone, 'waterway-label')
  })

  mapRef.value?.on('move', () => {
    // Update line size with zoom
    const zoom = mapRef.value?.getZoom()
    if (zoom) {
      // Update the line distance with the drone position
      // coordinate of the second point depending on yaw.
      const distance = 0.00015 * (Math.pow(2, 22 - zoom) / 8)
      const yaw = MathUtils.degToRad(sensorsStore.full.yaw)
      const lat = gpsPosition.value.lat
      const lng = gpsPosition.value.lng

      const newLng = lng + distance * Math.cos(yaw)
      const newLat = lat + distance * Math.sin(yaw)

      mapRef.value?.getSource('droneDirection').setData({
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'LineString',
          coordinates: [
            // Position of the drone
            [gpsPosition.value.lat, gpsPosition.value.lng],
            // Position of the direction last point of the drone
            [newLat, newLng]
          ]
        }
      })
    }
  })
})

const goToInitialZoom = () => {
  if (!mapRef.value) return
  mapRef.value?.setPitch(45)
  mapRef.value?.setBearing(0)
  mapRef.value?.zoomTo(15.75)
}
</script>
<template>
  <div class="relative h-full m-0 p-0 overflow-hidden">
    <div v-if="!loadMap" class="h-full w-full">
      <div
        class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
      >
        <div class="flex flex-col items-center">
          <div
            class="animate-spin rounded-full h-32 w-32 border-t-4 border-b-4 border-primary"
          ></div>
        </div>
      </div>
    </div>
    <MapboxMap
      v-else
      :map-id="`map-gps-${uniqueMapId}`"
      :options="{
        style: 'mapbox://styles/mapbox/satellite-streets-v12', // style URL
        pitch: 45,
        // center: [gpsPosition.lat, gpsPosition.lng], // starting position
        zoom: 15.75, // starting zoom,
        antialias: true,
        attributionControl: false
      }"
    >
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
        @click="toggleAttachedView"
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
      <button
        class="absolute top-[7.5rem] right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="toggle3dBuildings"
        title="Toggle 3D buildings"
      >
        <Box :size="24" />
      </button>
      <button
        class="absolute top-[10rem] right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="toggleMapView"
        title="Toggle map view"
      >
        <Map :size="24" />
      </button>
    </MapboxMap>
  </div>
</template>
