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
  <Overlay :show="isLoading">
    <SessionsDialog />
    <ReplaySession />
  </Overlay>
</template>

<style lang="scss"></style>
