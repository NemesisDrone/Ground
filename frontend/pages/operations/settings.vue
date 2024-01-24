<script setup lang="ts">
import { useDroneSettingsStore } from '~/store/droneSettings'
import { useToast } from '~/components/ui/toast'
import LogOut from '~/components/Operations/Settings/LogOut.vue'

definePageMeta({
  layout: 'sidebar',
  keepalive: false
})
useHead({
  title: 'Settings'
})

const isLoading = ref(false)
const droneSettingsStore = useDroneSettingsStore()
const localCanals = ref<{ canal: number; gpios: string }[]>([])

onMounted(async () => {
  await droneSettingsStore.getSettings()
  // localCanals.value = droneSettingsStore.canals.map((canal) => ({
  //   canal: canal.canal,
  //   gpios: canal.gpios.join(', ')
  // }))
})

const updateSettings = async () => {
  isLoading.value = true

  const canals = localCanals.value.map((canal) => ({
    canal: canal.canal,
    gpios: canal.gpios.split(',').map((gpio) => parseInt(gpio.trim()))
  }))
  await droneSettingsStore.updateSettings({ canals })

  useToast().toast({ title: 'Settings saved' })

  isLoading.value = false
}
</script>

<template>
  <div>
    <div class="p-4">
      <h1 class="text-3xl">Settings</h1>
      <p>
        TEMPORARY SETTINGS PAGE. This page will be developped/designed
        correctly later
      </p>
      <div class="w-[600px] mt-4">
        <UiTable>
          <UiTableHeader>
            <UiTableRow>
              <UiTableHead>Canal</UiTableHead>
              <UiTableHead>GPIOs</UiTableHead>
            </UiTableRow>
          </UiTableHeader>
          <UiTableBody>
            <UiTableRow v-for="canal in localCanals" :key="canal.canal">
              <UiTableCell>{{ canal.canal }}</UiTableCell>
              <UiTableCell><UiInput v-model="canal.gpios" /></UiTableCell>
            </UiTableRow>
          </UiTableBody>
        </UiTable>
        <div class="mt-4 flex justify-end">
          <UiButton @click="updateSettings" :is-loading="isLoading">
            Save Drone Settings
          </UiButton>
        </div>
      </div>
      <div class="mt-3">
        <LogOut />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss"></style>
