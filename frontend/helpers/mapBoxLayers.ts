import mapboxgl from 'mapbox-gl'
import {useSensorsStore} from '~/store/sensors'
import * as THREE from 'three'
import {MathUtils} from 'three'
// @ts-ignore
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js'
import {useReplayStore} from '~/store/replayStore'

/*
Get the mapbox layer for the drone model.
 */
export const getMapBox3DDroneModelLayer = (
  camera: THREE.Camera | null,
  scene: THREE.Scene | null,
  map: mapboxgl.Map,
  isForReplayMap: boolean
): mapboxgl.CustomLayerInterface => {
  const sensorStore = useSensorsStore()
  const replayStore = useReplayStore()

  /**
   *  When the map is for the replay, the gps position is the one of the current frame from replayStore.
   *  Otherwise, it's the one from the sensorStore, coming from the drone directly
   */
  const getDroneData = () => {
    if (isForReplayMap) {
      return {
        lat: replayStore.currentFrame.latitude,
        lng: replayStore.currentFrame.longitude,
        altitude: replayStore.currentFrame.altitude,
        roll: replayStore.currentFrame.roll,
        pitch: replayStore.currentFrame.pitch,
        yaw: replayStore.currentFrame.yaw
      }
    }

    return {
      lat: sensorStore.gpsPosition.lat,
      lng: sensorStore.gpsPosition.lng,
      altitude: sensorStore.altitude,
      roll: sensorStore.full.roll,
      pitch: sensorStore.full.pitch,
      yaw: sensorStore.full.yaw
    }
  }

  const layer: mapboxgl.CustomLayerInterface = {
    id: 'drone-model',
    type: 'custom',
    renderingMode: '3d',
    onAdd: function (map, gl) {
      camera = new THREE.Camera()
      scene = new THREE.Scene()

      // create two lights to illuminate the model
      const directionalLight = new THREE.DirectionalLight(0xffffff)
      directionalLight.position.set(0, -70, 100).normalize()
      scene.add(directionalLight)

      const directionalLight2 = new THREE.DirectionalLight(0xffffff)
      directionalLight2.position.set(0, 70, 100).normalize()
      scene.add(directionalLight2)

      //add the 3D model to the three scene
      const loader = new GLTFLoader()
      //  @ts-ignore
      loader.load('/mq-9_reaper/scene.gltf', (gltf) => {
        ;(scene as THREE.Scene).add(gltf.scene)
      })
      // @ts-ignore
      this.map = map
      // @ts-ignore
      this.renderer = new THREE.WebGLRenderer({
        canvas: map.getCanvas(),
        context: gl,
        antialias: true
      })

      // @ts-ignore
      this.renderer.autoClear = false
    },
    render: function (gl, matrix) {
      const droneData = getDroneData()
      const modelOrigin: [number, number] = [droneData.lat, droneData.lng]
      const modelAltitude = droneData.altitude
      const modelRotate = [
        MathUtils.degToRad(droneData.roll) + Math.PI / 2,
        -(MathUtils.degToRad(droneData.yaw) - Math.PI / 2),
        MathUtils.degToRad(droneData.pitch)
      ]

      const modelAsMercatorCoordinate =
        mapboxgl.MercatorCoordinate.fromLngLat(modelOrigin, modelAltitude)

      /*
      The factor variable is used to scale the size of the drone based on the zoom level.
       */
      const factor = Math.pow(2, 22 - map.getZoom()) / 8
      const scale =
        modelAsMercatorCoordinate.meterInMercatorCoordinateUnits() * factor

      /*
      When map zoom is less than 6, 3d model need to disappear.
      Otherwise drone is bugged.
      */
      if (map.getZoom() < 6) {
        return
      }

      const modelTransform = {
        translateX: modelAsMercatorCoordinate.x,
        translateY: modelAsMercatorCoordinate.y,
        translateZ: modelAsMercatorCoordinate.z as number,
        rotateX: modelRotate[0],
        rotateY: modelRotate[1],
        rotateZ: modelRotate[2],
        /* Since the 3D model is in real world meters, a scale transform needs to be applied
         */
        scale
      }

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

      const m = new THREE.Matrix4().fromArray(matrix)
      const l = new THREE.Matrix4()
        .makeTranslation(
          modelTransform.translateX,
          modelTransform.translateY,
          modelTransform.translateZ
        )
        .scale(
          new THREE.Vector3(
            modelTransform.scale,
            -modelTransform.scale,
            modelTransform.scale
          )
        )
        .multiply(rotationX)
        .multiply(rotationY)
        .multiply(rotationZ)

      // @ts-ignore
      camera.projectionMatrix = m.multiply(l)
      // @ts-ignore
      this.renderer.resetState()
      // @ts-ignore
      this.renderer.render(scene, camera)
      // @ts-ignore
      this.map.triggerRepaint()
    }
  }

  return layer
}

/**
 * Get the mapbox source for the drone direction
 */
export const getMapBoxDroneDirectionSourceData = (
  map: mapboxgl.Map,
  lat: number,
  lng: number,
  yaw: number
) => {
  const distance = 0.00015 * (Math.pow(2, 22 - (map.getZoom() || 0)) / 8)
  yaw = MathUtils.degToRad(yaw)
  const newLng = lng + distance * Math.cos(yaw)
  const newLat = lat + distance * Math.sin(yaw)

  return {
    type: 'Feature',
    properties: {},
    geometry: {
      type: 'LineString',
      coordinates: [
        // Position of the drone
        [lat, lng],
        // Position of the direction last point of the drone
        [newLat, newLng]
      ]
    }
  }
}
export const getMapBoxDroneDirectionLineLayer = (): mapboxgl.LineLayer => {
  return {
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
  }
}

export const addMapBoxTerrain = (map: mapboxgl.Map) => {
  map.addSource('mapbox-dem', {
    type: 'raster-dem',
    url: 'mapbox://mapbox.mapbox-terrain-dem-v1',
    tileSize: 512,
    maxzoom: 14
  })
  map.setTerrain({ source: 'mapbox-dem', exaggeration: 1 })
}

export const addMapBoxBuildingsLayer = (map: mapboxgl.Map) => {
  const layers = map.getStyle().layers
  // @ts-ignore
  const labelLayerId = layers.find(
    // @ts-ignore
    (layer) => layer.type === 'symbol' && layer.layout['text-field']
  ).id

  map.addLayer(
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
