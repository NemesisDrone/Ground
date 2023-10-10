<script lang="ts" setup>
import { io } from 'socket.io-client'
const config = useRuntimeConfig()
const socket = io(config.public.SOCKETIO_URL as string)

const GPSPosition = ref({ lat: 48.087912, lng: -0.756378 })
const GPSPositionHistory = ref<
  {
    lat: number
    lng: number
  }[]
>([])
const battery = ref(0)
const altitude = ref(0)
const isMapAttachedToDrone = ref(true)
const propulsorSpeed = ref(1)

socket.on('connect', () => {
  console.log('SocketIO connected')
})

socket.on('disconnect', () => {
  console.log('SocketIO disconnected')
})

socket.on('gps-position', (data) => {
  GPSPosition.value = data
})

socket.on('battery', (data) => {
  battery.value = data
})

socket.on('altitude', (data) => {
  altitude.value = data
})

socket.on('gps-position', (data) => {
  GPSPosition.value = data
  GPSPositionHistory.value.push(data)

  if (!mapRef.value || !markerRef.value) return

  markerRef.value.setLngLat([data.lng, data.lat])

  if (isMapAttachedToDrone.value)
    mapRef.value?.panTo([data.lng, data.lat], { duration: 1000 })
})

const goDown = () => {
  socket.emit('actions', 'actions:go-down')
}

const goUp = () => {
  socket.emit('actions', 'actions:go-up')
}

const goLeft = () => {
  socket.emit('actions', 'actions:go-left')
}

const goRight = () => {
  socket.emit('actions', 'actions:go-right')
}

const goForward = () => {
  socket.emit('actions', 'actions:go-forward')
}

const emitPropulsorSpeed = () => {
  socket.emit('actions', `actions:propulsor-speed,${propulsorSpeed.value}`)
}

const mapRef = useMapboxRef('map')
const markerRef = useMapboxMarkerRef('marker')

onMounted(() => {
  mapRef.value?.on('load', () => {
    const geoJsonGPSPositionHistory = {
      type: 'FeatureCollection',
      features: GPSPositionHistory.value.map((gpsPosition) => ({
        type: 'Feature',
        geometry: {
          type: 'LineString',
          coordinates: [gpsPosition.lng, gpsPosition.lat]
        }
      }))
    }
  })
})

watch(isMapAttachedToDrone, (newValue) => {
  if (!mapRef.value || !markerRef.value) return

  if (newValue) {
    mapRef.value?.panTo([GPSPosition.value.lng, GPSPosition.value.lat], {
      duration: 1000
    })
  }
})

onMounted(() => {
  window.addEventListener('keydown', (event) => {
    switch (event.key) {
      case 'ArrowUp':
        goUp()
        break
      case 'ArrowDown':
        goDown()
        break
      case 'ArrowLeft':
        goLeft()
        break
      case 'ArrowRight':
        goRight()
        break
    }
  })

  window.addEventListener('keyup', (event) => {
    console.log(event)
    switch (event.key) {
      case 'ArrowUp':
      case 'ArrowDown':
      case 'ArrowLeft':
      case 'ArrowRight':
        goForward()
        break
    }

    switch (event.code) {
      case 'Digit1':
        propulsorSpeed.value = 1
        emitPropulsorSpeed()
        break
      case 'Digit2':
        propulsorSpeed.value = 2
        emitPropulsorSpeed()
        break
      case 'Digit3':
        propulsorSpeed.value = 3
        emitPropulsorSpeed()
        break
      case 'Digit4':
        propulsorSpeed.value = 4
        emitPropulsorSpeed()
        break
      case 'Digit5':
        propulsorSpeed.value = 5
        emitPropulsorSpeed()
        break
      case 'Digit6':
        propulsorSpeed.value = 6
        emitPropulsorSpeed()
        break
      case 'Digit7':
        propulsorSpeed.value = 7
        emitPropulsorSpeed()
        break
      case 'Digit8':
        propulsorSpeed.value = 8
        emitPropulsorSpeed()
        break
      case 'Digit9':
        // propulsorSpeed.value = 9
        // emitPropulsorSpeed()
        break
    }
  })
})
</script>

<template>
  <div>
    <button @click="goDown">Go Down</button>
    <button @click="goUp">Go Up</button>
    <button @click="goLeft">Go Left</button>
    <button @click="goRight">Go Right</button>
    <button @click="goForward">Go Forward</button>
    <div style="display: flex; gap: 1rem">
      <p>Propulsor speed : {{ propulsorSpeed }}</p>
      <p>GPS Position: {{ GPSPosition }}</p>
      <p>Altitude : {{ altitude }}m</p>
      <p>Speed : 0km/h</p>
      <p>Orientation : {}</p>
      <p>Battery : {{ battery }}V</p>
    </div>

    <div style="display: flex; gap: 1rem">
      <div id="map-container">
        <MapboxMap
          map-id="map"
          :options="{
            style: 'mapbox://styles/mapbox/satellite-streets-v12', // style URL
            // style: 'mapbox://styles/mapbox/dark-v11',
            pitch: 60,
            center: [-0.7563779, 48.0879123], // starting position
            zoom: 16 // starting zoom
          }"
        >
          <button
            class="btn-attach-map"
            @click="isMapAttachedToDrone = !isMapAttachedToDrone"
          >
            {{ isMapAttachedToDrone ? 'Detach' : 'Attach' }}
          </button>
          <button class="btn-zoom-initial-map" @click="mapRef?.zoomTo(16)">
            Initial zoom
          </button>
          <MapboxDefaultMarker
            marker-id="marker"
            :lnglat="[GPSPosition.lng, GPSPosition.lat]"
          />
        </MapboxMap>
      </div>
      <div
        id="video-container"
        style="display: flex; justify-content: center; align-items: center"
      >
        No video found
      </div>
    </div>
  </div>
</template>

<style lang="scss">
#map-container {
  position: relative;
  height: 600px;
  width: 49vw;
  margin: 0;
  padding: 0;
  overflow: hidden;

  button.btn-attach-map {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 100;
    background-color: white;
    padding: 5px;
    border-radius: 5px;
    border: 1px solid white;
    cursor: pointer;
  }

  button.btn-zoom-initial-map {
    position: absolute;
    top: 10px;
    left: 90px;
    z-index: 100;
    background-color: white;
    padding: 5px;
    border-radius: 5px;
    border: 1px solid white;
    cursor: pointer;
  }
}

#video-container {
  position: relative;
  height: 600px;
  width: 49vw;
  margin: 0;
  padding: 0;
  overflow: hidden;
  border: 2px dashed rgba(0, 0, 0, 0.2);
  border-radius: 5px;
}
</style>
