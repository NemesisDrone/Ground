<script lang="ts" setup>
import ReplaySession from '~/components/Operations/Replay/ReplaySession.vue'
import SessionsDialog from '~/components/Operations/Replay/SessionsDialog.vue'
import { useReplayStore } from '~/store/replayStore'
import Overlay from '~/components/ui/overlay/Overlay.vue'

definePageMeta({
  layout: 'sidebar',
  keepalive: false
})
useHead({
  title: 'Replay'
})

const replayStore = useReplayStore()
const isLoading = ref(false)

onMounted(async () => {
  isLoading.value = true
  await replayStore.getSessions()
  isLoading.value = false

  // Open the dialog to select a session
  replayStore.isDialogSessionsOpen = true
})
</script>
<template>
  <SessionsDialog />
  <Overlay :show="isLoading" class="h-full">
    <ReplaySession v-if="replayStore.currentSession !== null" />
    <div
      v-else
      class="h-[100vh] flex flex-col justify-center items-center"
    >
      <div class="text-2xl">No session selected</div>
      <UiButton
        class="mt-4"
        @click="replayStore.isDialogSessionsOpen = true"
      >
        Select a session
      </UiButton>
    </div>
  </Overlay>
</template>

<style lang="scss"></style>
