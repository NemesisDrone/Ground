<script setup lang="ts">
import {
  ScreenShare,
  XCircle,
  LocateFixed,
  LocateOff,
  ScanSearch,
  Box
} from 'lucide-vue-next'
import { useSensorsStore } from '~/store/sensors'
import { storeToRefs } from 'pinia'
import { v4 as uuidv4 } from 'uuid'
import mapboxgl from 'mapbox-gl'
import * as THREE from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'

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
    // Set default center to esiea position
  }, 1500)
  setInterval(() => {
    pos.value += 0.00001
  }, 1000)
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

let scene: any = null
let camera: any = null
const pos = ref(-0.7563779)
watch(mapRef, () => {
  mapRef.value?.setCenter([gpsPosition.value.lat, gpsPosition.value.lng])
  mapRef.value?.on('style.load', () => {
    if (use3dBuildings.value) add3dBuildings()
  })

  const modelOrigin = [-0.7563779, 48.0879123]
  const modelAltitude = 10
  const modelRotate = [Math.PI / 2, 0, 0]

  const modelAsMercatorCoordinate = mapboxgl.MercatorCoordinate.fromLngLat(
    modelOrigin,
    modelAltitude
  )

  const modelTransform = {
    translateX: modelAsMercatorCoordinate.x,
    translateY: modelAsMercatorCoordinate.y,
    translateZ: modelAsMercatorCoordinate.z,
    rotateX: modelRotate[0],
    rotateY: modelRotate[1],
    rotateZ: modelRotate[2],
    /* Since the 3D model is in real world meters, a scale transform needs to be
     * applied since the CustomLayerInterface expects units in MercatorCoordinates.
     */
    scale: modelAsMercatorCoordinate.meterInMercatorCoordinateUnits() * 6
  }

  const customLayer = {
    id: '3d-model',
    type: 'custom',
    renderingMode: '3d',
    onAdd: function (map, gl) {
      camera = new THREE.Camera()
      scene = new THREE.Scene()

      // create two three.js lights to illuminate the model
      const directionalLight = new THREE.DirectionalLight(0xffffff)
      directionalLight.position.set(0, -70, 100).normalize()
      scene.add(directionalLight)

      const directionalLight2 = new THREE.DirectionalLight(0xffffff)
      directionalLight2.position.set(0, 70, 100).normalize()
      scene.add(directionalLight2)

      // use the three.js GLTF loader to add the 3D model to the three.js scene
      const loader = new GLTFLoader()
      loader.load('/mq-9_reaper/scene.gltf', (gltf) => {
        scene.add(gltf.scene)
      })
      this.map = map

      // use the Mapbox GL JS map canvas for three.js
      this.renderer = new THREE.WebGLRenderer({
        canvas: map.getCanvas(),
        context: gl,
        antialias: true
      })

      this.renderer.autoClear = false
    },
    render: function (gl, matrix) {
      const rotationX = new THREE.Matrix4().makeRotationAxis(
        new THREE.Vector3(1, 0, 0),
        modelTransform.rotateX
      )
      const rotationY = new THREE.Matrix4().makeRotationAxis(
        new THREE.Vector3(0, 1, 0),
        modelTransform.rotateY
      )
      const rotationZ = new THREE.Matrix4().makeRotationAxis(
        new THREE.Vector3(0, 0, 1),
        modelTransform.rotateZ
      )
      const modelAsMercatorCoordinate2 =
        mapboxgl.MercatorCoordinate.fromLngLat(
          [pos.value, modelOrigin[1]],
          modelAltitude
        )
      const modelTransform2 = {
        translateX: modelAsMercatorCoordinate2.x,
        translateY: modelAsMercatorCoordinate2.y,
        translateZ: modelAsMercatorCoordinate2.z,
        rotateX: modelRotate[0],
        rotateY: modelRotate[1],
        rotateZ: modelRotate[2],
        /* Since the 3D model is in real world meters, a scale transform needs to be
         * applied since the CustomLayerInterface expects units in MercatorCoordinates.
         */
        scale:
          modelAsMercatorCoordinate2.meterInMercatorCoordinateUnits() * 3
      }

      const m = new THREE.Matrix4().fromArray(matrix)
      const l = new THREE.Matrix4()
        .makeTranslation(
          modelTransform2.translateX,
          modelTransform2.translateY,
          modelTransform2.translateZ
        )
        .scale(
          new THREE.Vector3(
            modelTransform2.scale,
            -modelTransform2.scale,
            modelTransform2.scale
          )
        )
        .multiply(rotationX)
        .multiply(rotationY)
        .multiply(rotationZ)

      camera.projectionMatrix = m.multiply(l)
      this.renderer.resetState()
      this.renderer.render(scene, camera)
      this.map.triggerRepaint()
    }
  }
  mapRef.value?.on('style.load', () => {
    mapRef.value?.addLayer(customLayer, 'waterway-label')
  })
})

const goToInitialZoom = () => {
  if (!mapRef.value) return
  console.log('goToInitialZoom')
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
        // style: 'mapbox://styles/mapbox/satellite-streets-v12', // style URL
        style: 'mapbox://styles/mapbox/dark-v11',
        pitch: 45,
        // center: [gpsPosition.lat, gpsPosition.lng], // starting position
        zoom: 15.75, // starting zoom,
        antialias: true,
        attributionControl: false
      }"
    >
      <!--      <MapboxDefaultMarker-->
      <!--        marker-id="marker"-->
      <!--        :lnglat="[gpsPosition.lat, gpsPosition.lng]"-->
      <!--      />-->

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
      <button
        class="absolute top-[7.5rem] right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
        @click="toggle3dBuildings"
        title="Toggle 3D buildings"
      >
        <Box :size="24" />
      </button>
    </MapboxMap>
  </div>
</template>
