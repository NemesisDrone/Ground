<script setup lang="ts">
import { OrbitControls, GLTFModel, Sky } from '@tresjs/cientos'
import { Euler, Matrix4, Vector3, MathUtils } from 'three'
import { ShallowRef } from 'vue'
import { useComponentsStore } from '~/store/components'
import { useSensorsStore } from '~/store/sensors'

const componentsStore = useComponentsStore()
const sensorStore = useSensorsStore()
// @ts-ignore
const droneRef: ShallowRef<TresInstance | null> = shallowRef(null)

const droneModelAnimation = () => {
  if (droneRef.value && droneRef.value.value) {
    droneRef.value.value.rotation.x = MathUtils.degToRad(
      sensorStore.full.roll
    )
    droneRef.value.value.rotation.z = MathUtils.degToRad(
      sensorStore.full.pitch
    )
  }
  requestAnimationFrame(droneModelAnimation)
}

onMounted(() => {
  droneModelAnimation()
})
</script>
<template>
  <div
    class="rounded-md h-full p-2 bg-neutral-900"
    :class="`${
      componentsStore.connectionStatus.connected
        ? 'p-2'
        : 'border-2 border-red-600'
    }`"
  >
    <TresCanvas clear-color="#171717" shadows alpha>
      <TresPerspectiveCamera :position="[-9, 0, 0]" />
      <OrbitControls :enableRotate="true" />
      <Suspense>
        <GLTFModel ref="droneRef" path="/mq-9_reaper/scene.gltf" draco />
      </Suspense>
      <!--      <Sky :elevation="0.7" :azimuth="90" />-->
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
