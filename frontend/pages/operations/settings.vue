<script setup lang="ts">
import { useDroneSettingsStore } from '~/store/droneSettings'
import { useToast } from '~/components/ui/toast'
import { LogOut } from 'lucide-vue-next'
import { useUserStore } from '~/store/user'

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
  localCanals.value = droneSettingsStore.canals.map((canal) => ({
    canal: canal.canal,
    gpios: canal.gpios.join(', ')
  }))
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

const isLogOutLoading = ref(false)
const logOut = async () => {
  isLogOutLoading.value = true

  await useUserStore().logOut()
  useRouter().push('/?disconnected')

  isLogOutLoading.value = false
}
</script>

<template>
  <div>
    <div class="p-4">
      <h1 class="text-3xl">Settings</h1>
      <p>Temporary raw settings.</p>
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
        <UiDialog>
          <UiDialogTrigger>
            <UiButton variant="destructive">
              <LogOut :size="18" class="mr-2" />
              Log out
            </UiButton>
          </UiDialogTrigger>
          <UiDialogContent>
            <UiDialogHeader>
              <UiDialogTitle>Log out?</UiDialogTitle>
              <UiDialogDescription>
                You will be logged out. You can log in again.
              </UiDialogDescription>
            </UiDialogHeader>
            <UiDialogFooter>
              <UiButton
                variant="destructive"
                @click="logOut"
                :is-loading="isLogOutLoading"
              >
                Confirm
              </UiButton>
            </UiDialogFooter>
          </UiDialogContent>
        </UiDialog>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss"></style>
