<script setup lang="ts">
import { OrbitControls, GLTFModel, Sky } from '@tresjs/cientos'
import { Euler, Matrix4, Vector3, MathUtils, Quaternion } from 'three'
import { ShallowRef } from 'vue'
import { useComponentsStore } from '~/store/components'
import { useSensorsStore } from '~/store/sensors'
import { ScanSearch } from 'lucide-vue-next'

const componentsStore = useComponentsStore()
const sensorStore = useSensorsStore()
// @ts-ignore
const droneRef: ShallowRef<TresInstance | null> = shallowRef(null)
// @ts-ignore
const cameraRef: ShallowRef<TresInstance | null> = shallowRef(null)
const defaultCameraPosition = new Vector3(-9, 0, 0)
const defaultCameraLookAt = new Vector3(0, 0, 0)

const droneModelAnimation = () => {
  if (droneRef.value && droneRef.value.value) {
    // droneRef.value.value.rotation.x = MathUtils.degToRad(
    //   sensorStore.imu.roll
    // )
    // droneRef.value.value.rotation.z = MathUtils.degToRad(
    //   sensorStore.imu.pitch
    // )
    const imuQuaternion = new Quaternion(
      sensorStore.imu.quat[2],
      sensorStore.imu.quat[1],
      sensorStore.imu.quat[3],
      sensorStore.imu.quat[0]
    )
    droneRef.value.value.quaternion.copy(imuQuaternion)
  }
  requestAnimationFrame(droneModelAnimation)
}

onMounted(() => {
  droneModelAnimation()
})

const resetCameraPosition = () => {
  if (cameraRef.value) {
    cameraRef.value.position.set(
      defaultCameraPosition.x,
      defaultCameraPosition.y,
      defaultCameraPosition.z
    )
    cameraRef.value.lookAt(
      defaultCameraLookAt.x,
      defaultCameraLookAt.y,
      defaultCameraLookAt.z
    )
  }
}
</script>
<template>
  <div
    class="rounded-md h-full p-2 bg-neutral-900 relative"
    :class="`${
      componentsStore.connectionStatus.connected
        ? 'p-2'
        : 'border-2 border-red-600'
    }`"
  >
    <button
      class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
      @click="resetCameraPosition"
      title="Set camera position to default view"
    >
      <ScanSearch :size="24" />
    </button>
    <TresCanvas clear-color="#171717" shadows alpha>
      <TresPerspectiveCamera
        :position="defaultCameraPosition"
        ref="cameraRef"
      />
      <OrbitControls :enableRotate="true" />
      <Suspense>
        <GLTFModel ref="droneRef" path="/mq-9_reaper/scene.gltf" draco />
      </Suspense>
      <Stars />
      <TresGridHelper :rotate-x="1.5708" />
      <TresGridHelper />
      <TresDirectionalLight
        :position="[-4, 8, 4]"
        :intensity="1.5"
        cast-shadow
      />
    </TresCanvas>
  </div>
</template>

<style scoped lang="scss"></style>
