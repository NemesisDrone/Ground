<script setup lang="ts">
import {
  LocateFixed,
  LocateOff,
  ScanSearch,
  Box,
  Layers2,
  Tags
} from 'lucide-vue-next'
import { v4 as uuidv4 } from 'uuid'
import * as THREE from 'three'
import {
  addMapBoxBuildingsLayer,
  addMapBoxTerrain,
  getMapBox3DDroneModelLayer,
  getMapBoxDroneDirectionLineLayer,
  getMapBoxDroneDirectionSourceData
} from '~/helpers/mapBoxLayers'
import mapboxgl from 'mapbox-gl'
import { useReplayStore } from '~/store/replayStore'

const replayStore = useReplayStore()

const uniqueMapId = uuidv4()

const mapRef = useMapboxRef('map-gps-' + uniqueMapId)

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

const showLabels = ref(true)
const toggleLabels = () => {
  showLabels.value = !showLabels.value
  // @ts-ignore Im sorry but mapbox is typed like a pig
  mapRef.value?.style.stylesheet.layers.forEach(
    (layer: mapboxgl.Layer) => {
      if (layer.type === 'symbol') {
        mapRef.value?.setLayoutProperty(
          layer.id,
          'visibility',
          showLabels.value ? 'visible' : 'none'
        )
      }
    }
  )
}

const viewAttachedToDronePosition = ref(true)
watch(
  [
    () => replayStore.currentFrame.latitude,
    () => replayStore.currentFrame.longitude
  ],
  () => {
    if (!mapRef.value) return

    if (viewAttachedToDronePosition.value) {
      // Move the map to the drone position only if the drone position is not too far from the current position
      const distance = Math.abs(
        mapRef.value
          ?.getCenter()
          .distanceTo(
            new mapboxgl.LngLat(
              replayStore.currentFrame.latitude,
              replayStore.currentFrame.longitude
            )
          )
      )

      // Calcul of the max distance from the center of the map depending on the zoom
      const maxDistanceFromCenter =
        Math.pow(2, 22 - mapRef.value?.getZoom()) / 1.2

      if (distance > maxDistanceFromCenter) {
        mapRef.value?.panTo(
          [
            replayStore.currentFrame.latitude,
            replayStore.currentFrame.longitude
          ],
          {
            duration: 1000
          }
        )
      }
    }

    if (mapRef.value?.getSource('droneDirection')) {
      mapRef.value
        ?.getSource('droneDirection')
        // @ts-ignore Why does this function doesn't exist but exist ?
        .setData(
          getMapBoxDroneDirectionSourceData(
            mapRef.value,
            replayStore.currentFrame.latitude,
            replayStore.currentFrame.longitude,
            replayStore.currentFrame.yaw
          )
        )
    }
  }
)

const toggleAttachedView = () => {
  viewAttachedToDronePosition.value = !viewAttachedToDronePosition.value
  if (viewAttachedToDronePosition.value) {
    mapRef.value?.panTo(
      [
        replayStore.currentFrame.latitude,
        replayStore.currentFrame.longitude
      ],
      {
        duration: 1000
      }
    )
  }
}

const add3dBuildings = () => {
  addMapBoxBuildingsLayer(mapRef.value as mapboxgl.Map)
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
  // Center the map on the drone position, or default position
  mapRef.value.setCenter([
    replayStore.currentFrame.latitude,
    replayStore.currentFrame.longitude
  ])

  // Add drone model, custom layers... , buildings
  mapRef.value.on('style.load', () => {
    // Disable by default the labels
    toggleLabels()

    addMapBoxTerrain(mapRef.value as mapboxgl.Map)
    if (use3dBuildings.value) add3dBuildings()

    const layerDrone = getMapBox3DDroneModelLayer(
      camera,
      scene,
      mapRef.value as mapboxgl.Map,
      true
    )

    mapRef.value?.addSource('droneDirection', {
      type: 'geojson',
      data: getMapBoxDroneDirectionSourceData(
        mapRef.value,
        replayStore.currentFrame.latitude,
        replayStore.currentFrame.longitude,
        replayStore.currentFrame.yaw
      ) as any
    })

    mapRef.value?.addLayer(
      getMapBoxDroneDirectionLineLayer(),
      'waterway-label'
    )

    mapRef.value?.addLayer(layerDrone, 'waterway-label')
  })

  mapRef.value?.on('move', () => {
    if (!mapRef.value) return
    mapRef.value
      ?.getSource('droneDirection')
      // @ts-ignore Why does this function doesn't exist but exist ?
      .setData(
        getMapBoxDroneDirectionSourceData(
          mapRef.value,
          replayStore.currentFrame.latitude,
          replayStore.currentFrame.longitude,
          replayStore.currentFrame.yaw
        )
      )
  })
})

const goToInitialZoom = () => {
  if (!mapRef.value) return
  mapRef.value?.setPitch(45)
  mapRef.value?.setBearing(0)
  mapRef.value?.zoomTo(16.75)
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
        zoom: 16.75, // starting zoom,
        antialias: true,
        attributionControl: false
      }"
    >
      <button
        class="absolute top right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="toggleAttachedView"
        :title="viewAttachedToDronePosition ? 'Detach' : 'Attach'"
      >
        <LocateOff v-if="viewAttachedToDronePosition" :size="24" />
        <LocateFixed v-else :size="24" />
      </button>
      <button
        class="absolute top-10 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="goToInitialZoom"
        title="Go to initial zoom"
      >
        <ScanSearch :size="24" />
      </button>
      <button
        class="absolute top-20 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="toggle3dBuildings"
        title="Toggle 3D buildings"
      >
        <Box :size="24" />
      </button>
      <button
        class="absolute top-[7.5rem] right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="toggleMapView"
        title="Change map layer"
      >
        <Layers2 :size="24" />
      </button>
      <button
        class="absolute top-[10rem] right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="toggleLabels"
        title="Toggle labels"
      >
        <Tags :size="24" />
      </button>
    </MapboxMap>
  </div>
</template>
