<script setup lang="ts">
import { Wifi, WifiOff } from 'lucide-vue-next'
import { useComponentsStore } from '~/store/components'

const componentsStore = useComponentsStore()
</script>

<template>
  <div
    class="rounded bg-neutral-900 h-full flex flex-col items-center justify-center gap-0.5"
  >
    <Wifi
      v-if="componentsStore.connectionStatus.connected"
      :size="32"
      class="mt-1"
    />
    <WifiOff v-else :size="32" class="mt-1" />
    <h3
      class="text-xl font-bold"
      :class="`${
        componentsStore.connectionStatus.connected
          ? 'text-primary'
          : 'text-red-600'
      }`"
    >
      {{
        componentsStore.connectionStatus.connected
          ? 'Connected'
          : 'Disconnected'
      }}
    </h3>
    <p class="text-sm">Drone</p>
  </div>
</template>

<style scoped lang="scss"></style>
