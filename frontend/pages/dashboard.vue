<script lang="ts" setup>
import GPSMap from '~/components/Dashboard/GPSMap.vue'
import VideoStreaming from '~/components/Dashboard/VideoStreaming.vue'
import SpeedGauge from '~/components/Dashboard/SpeedGauge.vue'
import Altitude from '~/components/Dashboard/Altitude.vue'
import Battery from '~/components/Dashboard/Battery.vue'
import PropulsorSpeed from '~/components/Dashboard/PropulsorSpeed.vue'
import Camera from '~/components/Dashboard/Camera.vue'
import LogsViewer from '~/components/Dashboard/LogsViewer.vue'
import { Power, RotateCcw } from 'lucide-vue-next'
import { useDroneComponentsStore } from '~/store/droneComponents'
import ComponentStatus from '~/components/Dashboard/ComponentStatus.vue'
import DroneViewer from '~/components/Dashboard/DroneViewer.vue'

definePageMeta({
  // @ts-ignore
  layout: 'dashboard'
})

const droneComponentsStore = useDroneComponentsStore()

const send = () => {
  droneComponentsStore.websocket?.send({
    route: 'state:stop:TestCompo',
    data: {
      component: 'TestCompo'
    }
  })
}
</script>

<template>
  <div class="w-full h-full flex min-h-[100vh]">
    <div class="w-3/5 p-4">
      <div class="w-full h-1/6 flex gap-4">
        <div class="w-full h-full">
          <SpeedGauge />
        </div>
        <div class="w-full h-full">
          <Altitude />
        </div>
        <div class="w-full h-full">
          <Battery />
        </div>
        <div class="w-full h-full">
          <PropulsorSpeed />
        </div>
        <div class="w-full h-full">
          <Camera />
        </div>
      </div>

      <div class="h-3/6 flex w-full gap-4">
        <div class="w-1/2 py-4">
          <DroneViewer />
        </div>
        <div class="w-1/2">
          <UiButton class="mt-7" @click="send">test</UiButton>
        </div>
      </div>

      <div class="h-2/6 w-full flex gap-4" style="max-height: 33.33vh">
        <div class="w-1/2">
          <LogsViewer />
        </div>
        <div class="w-1/2 grid grid-cols-4 gap-4">
          <ComponentStatus :component="droneComponentsStore.gps" />
          <ComponentStatus :component="droneComponentsStore.barometer" />
          <ComponentStatus
            :component="droneComponentsStore.batteryReader"
          />
          <ComponentStatus
            :component="droneComponentsStore.propulsionController"
          />
          <ComponentStatus
            :component="droneComponentsStore.propulsionController"
          />
          <ComponentStatus
            :component="droneComponentsStore.servoController"
          />
          <ComponentStatus
            :component="droneComponentsStore.propulsionController"
          />
          <ComponentStatus
            :component="droneComponentsStore.servoController"
          />
        </div>
      </div>
    </div>
    <div class="w-2/5 p-2">
      <div class="w-full h-1/2 pb-1">
        <GPSMap />
      </div>
      <div class="w-full h-1/2 pt-1">
        <VideoStreaming />
      </div>
    </div>
  </div>
</template>

<style lang="scss"></style>
