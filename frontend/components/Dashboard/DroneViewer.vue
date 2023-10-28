<script setup lang="ts">
import { OrbitControls, GLTFModel, Sky } from '@tresjs/cientos'
import { ShallowRef } from 'vue'
import { useDroneComponentsStore } from '~/store/droneComponents'

const droneComponentsStore = useDroneComponentsStore()
// @ts-ignore
const droneRef: ShallowRef<TresInstance | null> = shallowRef(null)
// @ts-ignore
const verticalGrids: ShallowRef<TresInstance | null> = shallowRef(null)

let interval: NodeJS.Timeout | null = null
const speed = ref(0.005)
const sens = ref(0)

onMounted(() => {
  interval = setInterval(() => {
    if (!droneComponentsStore.connectionStatus.connected) {
      droneRef.value.value.rotation.x = 0
      droneRef.value.value.rotation.z = 0
      return
    }
    if (droneRef.value && droneRef.value.value) {
      if (sens.value === 0) {
        droneRef.value.value.rotation.x += speed.value

        if (droneRef.value.value.rotation.x > 0.5) {
          sens.value = 1
        }
      } else if (sens.value === 1) {
        droneRef.value.value.rotation.x -= speed.value

        if (droneRef.value.value.rotation.x < -0.5) {
          sens.value = 2
        }
      } else if (sens.value === 2) {
        droneRef.value.value.rotation.x += speed.value

        if (droneRef.value.value.rotation.x >= 0) {
          sens.value = 3
        }
      } else if (sens.value === 3) {
        droneRef.value.value.rotation.z += speed.value

        if (droneRef.value.value.rotation.z > 0.5) {
          sens.value = 4
        }
      } else if (sens.value === 4) {
        droneRef.value.value.rotation.z -= speed.value

        if (droneRef.value.value.rotation.z < -0.5) {
          sens.value = 5
        }
      } else if (sens.value === 5) {
        droneRef.value.value.rotation.z += speed.value

        if (droneRef.value.value.rotation.z >= 0) {
          sens.value = 0
        }
      }
    }
  }, 10)
})

onUnmounted(() => {
  clearInterval(interval!)
})
</script>
<template>
  <div
    class="rounded-md h-full p-2 bg-neutral-900"
    :class="`${
      droneComponentsStore.connectionStatus.connected
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
