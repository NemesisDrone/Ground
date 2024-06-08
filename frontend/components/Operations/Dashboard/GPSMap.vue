<script setup lang="ts">
import {
  ScreenShare,
  XCircle,
  LocateFixed,
  LocateOff,
  ScanSearch,
  Box,
  Layers2,
  Tags,
  Goal,
  PlayCircle,
  Mountain,
  SendHorizontal
} from 'lucide-vue-next'
import { useSensorsStore } from '~/store/sensors'
import { storeToRefs } from 'pinia'
import { v4 as uuidv4 } from 'uuid'
import * as THREE from 'three'
import {
  addMapBoxBuildingsLayer,
  addMapBoxTerrain,
  getMapBox3DDroneModelLayer,
  getMapBoxDroneDirectionLineLayer,
  getMapBoxDroneDirectionSourceData
} from '~/helpers/mapBoxLayers'
import { MathUtils } from 'three'
import mapboxgl from 'mapbox-gl'
import { useDroneSettingsStore } from '~/store/droneSettings'

const droneStore = useDroneSettingsStore()

const props = defineProps<{
  enableAltitudeManipulation?: boolean
}>()

const sensorsStore = useSensorsStore()
const { gpsPosition, altitude } = storeToRefs(sensorsStore)

const uniqueMapId = uuidv4()

const mapRef = useMapboxRef('map-gps-' + uniqueMapId)
const directionPopupRef = useMapboxPopupRef('direction-popup')
const route = useRoute()

const popupDirectionPosition = ref({
  lat: 0,
  lng: 0
})
const showPopupDirection = ref(false)

const localObjectiveAltitude = ref(droneStore.objectives.altitude)

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
watch(gpsPosition, () => {
  if (!mapRef.value) return

  if (viewAttachedToDronePosition.value) {
    // Move the map to the drone position only if the drone position is not too far from the current position
    const distance = Math.abs(
      mapRef.value
        ?.getCenter()
        .distanceTo(
          new mapboxgl.LngLat(gpsPosition.value.lat, gpsPosition.value.lng)
        )
    )

    // Calcul of the max distance from the center of the map depending on the zoom
    const maxDistanceFromCenter =
      Math.pow(2, 22 - mapRef.value?.getZoom()) / 1.2

    if (distance > maxDistanceFromCenter) {
      mapRef.value?.panTo([gpsPosition.value.lat, gpsPosition.value.lng], {
        duration: 1000
      })
    }
  }

  if (mapRef.value?.getSource('droneDirection')) {
    mapRef.value
      ?.getSource('droneDirection')
      // @ts-ignore Why does this function doesn't exist but exist ?
      .setData(
        getMapBoxDroneDirectionSourceData(
          mapRef.value,
          gpsPosition.value.lat,
          gpsPosition.value.lng,
          sensorsStore.imu.yaw
        )
      )
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
  mapRef.value.setCenter([gpsPosition.value.lat, gpsPosition.value.lng])

  // Add drone model, custom layers... , buildings
  mapRef.value.on('style.load', () => {
    addMapBoxTerrain(mapRef.value as mapboxgl.Map)
    if (use3dBuildings.value) add3dBuildings()

    const layerDrone = getMapBox3DDroneModelLayer(
      camera,
      scene,
      mapRef.value as mapboxgl.Map,
      false
    )

    mapRef.value?.addSource('droneDirection', {
      type: 'geojson',
      data: getMapBoxDroneDirectionSourceData(
        mapRef.value,
        gpsPosition.value.lat,
        gpsPosition.value.lng,
        sensorsStore.imu.yaw
      ) as any
    })

    mapRef.value?.addLayer(
      getMapBoxDroneDirectionLineLayer(),
      'waterway-label'
    )

    mapRef.value?.addLayer(layerDrone, 'waterway-label')

    mapRef.value?.on('click', (e) => {
      popupDirectionPosition.value = {
        lat: e.lngLat.lat,
        lng: e.lngLat.lng
      }
      showPopupDirection.value = true
    })
  })

  mapRef.value?.on('move', () => {
    if (!mapRef.value) return
    try {
      mapRef.value
        ?.getSource('droneDirection')
        // @ts-ignore Why does this function doesn't exist but exist ?
        .setData(
          getMapBoxDroneDirectionSourceData(
            mapRef.value,
            gpsPosition.value.lat,
            gpsPosition.value.lng,
            sensorsStore.imu.yaw
          )
        )
    } catch {}
  })
})

watch(directionPopupRef, () => {
  if (!directionPopupRef.value) return

  // @ts-ignore _content
  directionPopupRef.value._content.querySelector('#btn-position').onclick =
    updateDirection
})
const goToInitialZoom = () => {
  if (!mapRef.value) return
  mapRef.value?.setPitch(45)
  mapRef.value?.setBearing(0)
  mapRef.value?.zoomTo(15.75)
}

const updateDirection = () => {
  showPopupDirection.value = false
  droneStore.objectives.droneDirection = {
    ...popupDirectionPosition.value
  }
  droneStore.updateDroneObjectives()
}

const updateAltitudeObjective = () => {
  droneStore.objectives.altitude = localObjectiveAltitude.value
  droneStore.updateDroneObjectives()
}

const isObjectAltitudeInRange = computed(() => {
  return (
    MathUtils.clamp(
      altitude.value,
      droneStore.objectives.altitude - 2,
      droneStore.objectives.altitude + 2
    ) === altitude.value
  )
})
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
      <div
        v-if="props.enableAltitudeManipulation"
        class="absolute top-0 left-0 z-50 bg-neutral-900 rounded p-4 mt-2.5 ml-2.5 text-primary w-[250px]"
      >
        <div class="flex justify-between items-center">
          <Mountain :size="22" class="text-white" />
          <h3
            class="text-xl text-primary font-bold"
            :class="{ 'text-red-600': !isObjectAltitudeInRange }"
          >
            {{ altitude }}/{{ droneStore.objectives.altitude }} m
          </h3>
        </div>
        <div class="flex mt-3 gap-2">
          <UiInput
            id="altitude-objectif"
            placeholder="Altitude objective"
            autocomplete="off"
            type="number"
            class="w-full"
            v-model="localObjectiveAltitude"
          />
          <UiButton class="scale-[0.9]" @click="updateAltitudeObjective">
            <SendHorizontal :size="18" />
          </UiButton>
        </div>
      </div>
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
        title="Change map layer"
      >
        <Layers2 :size="24" />
      </button>
      <button
        class="absolute top-[12.5rem] right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="toggleLabels"
        title="Toggle labels"
      >
        <Tags :size="24" />
      </button>
      <MapboxDefaultPopup
        v-if="showPopupDirection"
        popup-id="direction-popup"
        :lnglat="[popupDirectionPosition.lng, popupDirectionPosition.lat]"
        :options="{ closeOnClick: false }"
      >
        <div class="text-black">
          <UiButton id="btn-position" class="flex items-center gap-2">
            <Goal :size="24" />
            <span>Change objectif</span>
          </UiButton>
        </div>
      </MapboxDefaultPopup>
      <MapboxDefaultMarker
        marker-id="drone-position-objectif"
        :lnglat="[
          droneStore.objectives.droneDirection.lng,
          droneStore.objectives.droneDirection.lat
        ]"
        :options="{ color: '#22C55E' }"
      />
    </MapboxMap>
  </div>
</template>
