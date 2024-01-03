import mapboxgl, { CustomLayerInterface } from 'mapbox-gl'
import { useSensorsStore } from '~/store/sensors'
import * as THREE from 'three'
// @ts-ignore
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { MathUtils } from 'three'

export const getMapBox3DDroneModelLayer = (
  camera: THREE.Camera | null,
  scene: THREE.Scene | null,
  map: mapboxgl.Map
): mapboxgl.CustomLayerInterface => {
  const sensorStore = useSensorsStore()

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
      const modelOrigin: [number, number] = [
        sensorStore.gpsPosition.lat,
        sensorStore.gpsPosition.lng
      ]
      const modelAltitude = sensorStore.altitude
      const modelRotate = [
        MathUtils.degToRad(sensorStore.full.roll) + Math.PI / 2,
        -(MathUtils.degToRad(sensorStore.full.yaw) - Math.PI / 2),
        MathUtils.degToRad(sensorStore.full.pitch)
      ]

      const modelAsMercatorCoordinate =
        mapboxgl.MercatorCoordinate.fromLngLat(modelOrigin, modelAltitude)

      /*
      The factor variable is used to scale the size of the drone based on the zoom level.
       */
      const factor = Math.pow(2, 22 - map.getZoom()) / 11
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

export const getMapBoxDroneDirectionLineLayer = (): mapboxgl.LineLayer => {
  const sensorStore = useSensorsStore()

  const layer: mapboxgl.LineLayer = {
    id: 'drone-direction',
    type: 'line',
    source: {
      type: 'geojson',
      // @ts-ignore
      data: {
        type: 'Feature',
        geometry: {
          type: 'LineString',
          // @ts-ignore
          coordinates: [
            [sensorStore.gpsPosition.lng, sensorStore.gpsPosition.lat],
            [
              sensorStore.gpsPosition.lng + 0.0001,
              sensorStore.gpsPosition.lat + 0.0001
            ]
          ]
        }
      }
    },
    paint: {
      'line-color': '#FF0000',
      'line-width': 2
    }
  }

  return layer
}
