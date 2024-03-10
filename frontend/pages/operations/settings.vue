<script setup lang="ts">
import { useDroneSettingsStore } from '~/store/droneSettings'
import { useToast } from '~/components/ui/toast'
import LogOut from '~/components/Operations/Settings/LogOut.vue'
import { Model } from '~/types/droneSettings.types'

/**
 * This page has to be entirely reworked.
 * I've just made it as a raw design page to test the models/settings update.
 * A lot of good UI/UX things are missing, like a confirmation dialog before deleting a model, or ....
 * That's normal.
 */

definePageMeta({
  layout: 'sidebar',
  keepalive: false
})
useHead({
  title: 'Settings'
})

const isLoading = ref(false)
const droneSettingsStore = useDroneSettingsStore()

interface LocalModel
  extends Omit<Model, 'servo_canals' | 'brushless_canals'> {
  servo_canals: { canal: number; gpios: string }[]
  brushless_canals: { canal: number; gpios: string }[]
}

const localModels = ref<LocalModel[]>([])

const getSettings = async () => {
  isLoading.value = true
  await droneSettingsStore.getSettings()

  localModels.value = droneSettingsStore.models.map((model) => ({
    ...model,
    servo_canals: model.servo_canals.map((canal) => ({
      canal: canal.canal,
      gpios: canal.gpios.join(';')
    })),
    brushless_canals: model.brushless_canals.map((canal) => ({
      canal: canal.canal,
      gpios: canal.gpios.join(';')
    }))
  }))
  isLoading.value = false
}

onMounted(async () => {
  await getSettings()
})

const updateDroneSettingsModel = async (model: LocalModel) => {
  isLoading.value = true

  /**
   * Parse the model to remove the gpios string and replace it by an array of gpios
   */
  const parsedModel: Model = {
    ...model,
    servo_canals: model.servo_canals.map((canal) => ({
      canal: canal.canal,
      gpios: canal.gpios
        .split(';')
        .map((gpio) => parseInt(gpio.trim()))
        .filter((gpio) => !isNaN(gpio))
    })),
    brushless_canals: model.brushless_canals.map((canal) => ({
      canal: canal.canal,
      gpios: canal.gpios
        .split(';')
        .map((gpio) => parseInt(gpio.trim()))
        .filter((gpio) => !isNaN(gpio))
    }))
  }

  await droneSettingsStore.updateDroneModel(parsedModel)

  useToast().toast({ title: 'Model saved' })

  isLoading.value = false
}

const deleteDroneSettingsModel = async (model: LocalModel) => {
  isLoading.value = true
  await droneSettingsStore.deleteDroneModel(model.id)
  await getSettings()
  isLoading.value = false
}

const newModel = ref<LocalModel>({
  id: 0,
  name: '',
  servo_canals: [
    { canal: 1, gpios: '' },
    { canal: 2, gpios: '' },
    { canal: 3, gpios: '' },
    { canal: 4, gpios: '' },
    { canal: 5, gpios: '' },
    { canal: 6, gpios: '' },
    { canal: 7, gpios: '' },
    { canal: 8, gpios: '' },
    { canal: 9, gpios: '' },
    { canal: 10, gpios: '' }
  ],
  brushless_canals: [
    { canal: 1, gpios: '' },
    { canal: 2, gpios: '' },
    { canal: 3, gpios: '' },
    { canal: 4, gpios: '' },
    { canal: 5, gpios: '' },
    { canal: 6, gpios: '' },
    { canal: 7, gpios: '' },
    { canal: 8, gpios: '' },
    { canal: 9, gpios: '' },
    { canal: 10, gpios: '' }
  ],
  drone_settings: 0
})

const createDroneSettingsModel = async () => {
  if (newModel.value.name === '') return
  isLoading.value = true

  /**
   * Parse the model to remove the gpios string and replace it by an array of gpios
   */
  const parsedModel: Model = {
    id: 0,
    name: newModel.value.name,
    servo_canals: newModel.value.servo_canals.map((canal) => ({
      canal: canal.canal,
      gpios: canal.gpios
        .split(';')
        .map((gpio) => parseInt(gpio.trim()))
        .filter((gpio) => !isNaN(gpio))
    })),
    brushless_canals: newModel.value.brushless_canals.map((canal) => ({
      canal: canal.canal,
      gpios: canal.gpios
        .split(';')
        .map((gpio) => parseInt(gpio.trim()))
        .filter((gpio) => !isNaN(gpio))
    })),
    drone_settings: droneSettingsStore.id
  }

  try {
    await droneSettingsStore.createDroneModel(parsedModel)
    await getSettings()

    useToast().toast({ title: 'Model created' })
  } catch (e) {
    useToast().toast({ title: 'Model name already exists' })
  }

  isLoading.value = false
}

const updateSelectedDroneModel = async (model: LocalModel) => {
  isLoading.value = true
  await droneSettingsStore.updateSelectedDroneModel(model.id)
  await getSettings()

  useToast().toast({ title: `${model.name} selected` })
  isLoading.value = false
}
</script>

<template>
  <UiOverlay :show="isLoading">
    <div class="p-4">
      <h1 class="text-3xl">Settings</h1>
      <p class="text-red-500">
        RAW SETTINGS PAGE. This page will be developped/designed correctly
        later. For now, it's just a raw page to test the settings.
      </p>

      <div class="flex mt-4 gap-4 items-center">
        <div class="flex flex-col">
          <h3 class="text-xl">Models</h3>
          <p v-if="droneSettingsStore.selected_drone_model">
            Currently selected:
            {{ droneSettingsStore.selected_drone_model.name }}
          </p>
        </div>
        <UiDialog>
          <UiDialogTrigger>
            <UiButton> Create model</UiButton>
          </UiDialogTrigger>
          <UiDialogContent>
            <UiDialogHeader>
              <UiDialogTitle> Create a model</UiDialogTitle>
            </UiDialogHeader>

            <div class="grid space-y-1">
              <UiLabel>Model name</UiLabel>
              <UiInput v-model="newModel.name" />
            </div>

            <UiDialogFooter>
              <UiDialogClose as-child>
                <UiButton @click="createDroneSettingsModel()">
                  Create
                </UiButton>
              </UiDialogClose>
            </UiDialogFooter>
          </UiDialogContent>
        </UiDialog>
      </div>
      <div class="grid grid-cols-3 gap-4 mt-4">
        <div
          v-for="model in localModels"
          class="rounded bg-neutral-900 p-4"
        >
          <div class="grid space-y-1">
            <UiLabel>Model name</UiLabel>
            <UiInput v-model="model.name" />
          </div>

          <UiTable class="mt-4">
            <UiTableHeader>
              <UiTableRow>
                <UiTableHead>Canal</UiTableHead>
                <UiTableHead>GPIOs Servo</UiTableHead>
                <UiTableHead>GPIOs Brushless motor</UiTableHead>
              </UiTableRow>
            </UiTableHeader>
            <UiTableBody>
              <UiTableRow v-for="i in 10">
                <UiTableCell>{{ i }}</UiTableCell>
                <UiTableCell>
                  <UiInput v-model="model.servo_canals[i - 1].gpios" />
                </UiTableCell>
                <UiTableCell>
                  <UiInput v-model="model.brushless_canals[i - 1].gpios" />
                </UiTableCell>
              </UiTableRow>
            </UiTableBody>
          </UiTable>

          <UiLabel class="mt-4"> FlightMode Channel</UiLabel>
          <UiInput
            class="mt-2"
            v-model="model.flight_mode_channel"
            placeholder="FlightMode Channel"
          />

          <div class="mt-4 flex justify-end gap-4">
            <UiButton
              variant="destructive"
              @click="deleteDroneSettingsModel(model)"
            >
              Delete
            </UiButton>
            <UiButton @click="updateSelectedDroneModel(model)">
              Select
            </UiButton>
            <UiButton @click="updateDroneSettingsModel(model)">
              Save
            </UiButton>
          </div>
        </div>
      </div>
      <div class="mt-4">
        <LogOut />
      </div>
    </div>
  </UiOverlay>
</template>

<style scoped lang="scss"></style>
