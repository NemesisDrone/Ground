<script lang="ts" setup>
import GPSMap from '~/components/Operations/GPSMap.vue'
import VideoStreaming from '~/components/Operations/VideoStreaming.vue'
import SpeedGauge from '~/components/Operations/SpeedGauge.vue'
import Altitude from '~/components/Operations/Altitude.vue'
import Battery from '~/components/Operations/Battery.vue'
import PropulsorSpeed from '~/components/Operations/PropulsorSpeed.vue'
import LogsViewer from '~/components/Operations/LogsViewer.vue'
import { useComponentsStore } from '~/store/components'
import ComponentStatus from '~/components/Operations/ComponentStatus.vue'
import DroneViewer from '~/components/Operations/DroneViewer.vue'
import DroneStatusConnection from '~/components/Operations/DroneStatusConnection.vue'
import {
  Gamepad2,
  Locate,
  Mountain,
  PlaneTakeoff,
  PlugZap
} from 'lucide-vue-next'
import { useSensorsStore } from '~/store/sensors'

definePageMeta({
  layout: 'sidebar',
  keepalive: false
})
useHead({
  title: 'Dashboard'
})

const componentsStore = useComponentsStore()
const sensorsStore = useSensorsStore()
const stop = () => {
  componentsStore.websocket?.send({
    route: 'state:stop:gps',
    data: {
      component: 'gps'
    }
  })
}
const start = () => {
  componentsStore.websocket?.send({
    route: 'state:start:gps',
    data: {
      component: 'gps'
    }
  })
}

const demoSpeed = (value: number) => {
  componentsStore.websocket?.send({
    route: 'propulsion:speed',
    data: value
  })
}

const demoCalibrate = () => {
  componentsStore.websocket?.send({
    route: 'propulsion:calibrate',
    data: null
  })
}

const demoArm = () => {
  componentsStore.websocket?.send({
    route: 'propulsion:arm',
    data: null
  })
}

const demoDisarm = () => {
  componentsStore.websocket?.send({
    route: 'propulsion:disarm',
    data: null
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
          <DroneStatusConnection />
        </div>
      </div>

      <div class="h-3/6 flex w-full gap-4">
        <div class="w-1/2 py-4">
          <DroneViewer />
        </div>
        <div class="w-1/2">
          <UiButton class="mt-7" @click="demoSpeed(0)">0</UiButton>
          <UiButton class="mt-7 ml-2" @click="demoSpeed(800)"
            >800</UiButton
          >
          <UiButton class="mt-7 ml-2" @click="demoSpeed(1100)"
            >1100</UiButton
          >
          <UiButton class="mt-7 ml-2" @click="demoSpeed(1500)"
            >1500</UiButton
          >
          <UiButton class="mt-7 ml-2" @click="demoSpeed(1800)"
            >1800</UiButton
          >
          <UiButton class="mt-7 ml-2" @click="demoSpeed(2100)"
            >2100</UiButton
          >
          <UiButton class="ml-2 mt-2" @click="demoSpeed(2500)">
            2500
          </UiButton>
          <UiButton class="ml-2 mt-2" @click="demoCalibrate">
            Calibrate
          </UiButton>
          <UiButton class="ml-2 mt-2" @click="demoArm"> Arm </UiButton>
          <UiButton class="ml-2 mt-2" @click="demoDisarm">
            Disarm
          </UiButton>
          <br />
          {{ componentsStore.connectionStatus }}
          <br />
          {{ componentsStore.controller.axes }}
          {{ sensorsStore.full }}
        </div>
      </div>

      <div class="h-2/6 w-full flex gap-4" style="max-height: 33.33vh">
        <div class="w-1/2">
          <LogsViewer />
        </div>
        <div class="w-1/2 grid grid-cols-4 gap-4">
          <ComponentStatus
            :component="componentsStore.gps"
            :icon="Locate"
          />
          <ComponentStatus :component="componentsStore.servoController" />
          <ComponentStatus
            :component="componentsStore.barometer"
            :icon="Mountain"
          />
          <ComponentStatus
            :component="componentsStore.batteryReader"
            :icon="PlugZap"
          />
          <ComponentStatus
            :component="componentsStore.propulsionController"
            :icon="PlaneTakeoff"
          />
          <ComponentStatus :component="componentsStore.servoController" />
          <ComponentStatus
            :component="componentsStore.laserDistanceSensor"
          />
          <ComponentStatus
            :component="componentsStore.controller"
            :icon="Gamepad2"
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
