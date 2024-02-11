<script setup lang="ts">
import { Settings } from 'lucide-vue-next'
import { useReplayStore } from '~/store/replayStore'
import Overlay from '~/components/ui/overlay/Overlay.vue'

const replayStore = useReplayStore()
const isDialogOpen = ref(false)
const isLoading = ref(false)
const sessionName = ref('')

watch(isDialogOpen, () => {
  if (isDialogOpen.value && replayStore.currentSession)
    sessionName.value = replayStore.currentSession.name
})
const updateSessionName = async () => {
  isLoading.value = true

  if (replayStore.currentSession) {
    await replayStore.updateSessionName(
      replayStore.currentSession.id,
      sessionName.value
    )
    replayStore.currentSession.name = sessionName.value
  }

  isLoading.value = false
  replayStore.getSessions()

  isDialogOpen.value = false
}
</script>

<template>
  <UiDialog :open="isDialogOpen" @update:open="isDialogOpen = $event">
    <UiDialogTrigger as-child>
      <div
        class="rounded bg-neutral-900 items-center justify-center hover:bg-neutral-800 cursor-pointer"
      >
        <Settings :size="22" class="m-2" />
      </div>
    </UiDialogTrigger>
    <UiDialogContent>
      <Overlay :show="isLoading">
        <UiDialogHeader>
          <UiDialogTitle>Settings</UiDialogTitle>
        </UiDialogHeader>

        <div class="grid space-y-2 mt-4">
          <UiLabel>Name of the session</UiLabel>
          <UiInput v-model="sessionName" placeholder="Session name" />
        </div>

        <UiDialogFooter class="mt-4">
          <UiButton @click="updateSessionName"> Save </UiButton>
        </UiDialogFooter>
      </Overlay>
    </UiDialogContent>
  </UiDialog>
</template>

<style scoped lang="scss"></style>
