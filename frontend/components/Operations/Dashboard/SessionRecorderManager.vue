<script setup lang="ts">
import { PlayCircle, PauseCircle, StopCircle } from 'lucide-vue-next'
import { useComponentsStore } from '~/store/components'
import { useReplayStore } from '~/store/replayStore'
import { formatTimer } from '~/helpers/utils'
import { MessageEvent } from '~/helpers/webSocketWrapper'

const componentsStore = useComponentsStore()
const replayStore = useReplayStore()

/*
 *  Recording action  used in the UI on buttons
 */
const actions = {
  start: () => {
    componentsStore.communicationWebsocket?.send({
      route: 'recorder:start',
      data: null
    })
  },
  stop: () => {
    componentsStore.communicationWebsocket?.send({
      route: 'recorder:stop',
      data: null
    })
  },
  pause: () => {
    componentsStore.communicationWebsocket?.send({
      route: 'recorder:pause',
      data: null
    })
  }
}

/*
 *  Handle the recording time in seconds
 */
const interval = setInterval(() => {
  if (replayStore.recorder.isRecording && !replayStore.recorder.isPaused) {
    replayStore.recorder.recordingSince++
  }
}, 1000)

onUnmounted(() => {
  clearInterval(interval)
})

onMounted(() => {
  componentsStore.communicationWebsocket?.onMessage(
    'recorder:status',
    (
      event: MessageEvent<{
        is_recording: boolean
        is_paused: boolean
      }>
    ) => {
      replayStore.recorder.isRecording = event.data.is_recording
      replayStore.recorder.isPaused = event.data.is_paused
      if (!event.data.is_recording) replayStore.recorder.recordingSince = 0
    }
  )
})
</script>

<template>
  <div class="rounded bg-neutral-900 h-full p-4 flex flex-col">
    <h4>Session recorder</h4>
    <div class="flex mt-2 justify-between items-center">
      <div class="flex gap-2">
        <UiButton
          v-show="
            replayStore.recorder.isPaused ||
            !replayStore.recorder.isRecording
          "
          @click="actions.start"
        >
          <span class="flex items-center gap-2">
            <PlayCircle :size="20" />
            <span>{{
              replayStore.recorder.isPaused ? 'Resume' : 'Start'
            }}</span>
          </span>
        </UiButton>
        <UiButton
          v-show="
            replayStore.recorder.isRecording &&
            !replayStore.recorder.isPaused
          "
          @click="actions.pause"
        >
          <span class="flex items-center gap-2">
            <PauseCircle :size="20" />
            <span>Pause</span>
          </span>
        </UiButton>
        <UiButton
          v-show="replayStore.recorder.isRecording"
          variant="destructive"
          @click="actions.stop"
        >
          <span class="flex items-center gap-2">
            <StopCircle :size="20" />
            <span>Stop</span>
          </span>
        </UiButton>
      </div>
      <div>
        <span
          v-if="!replayStore.recorder.isRecording"
          class="text-red-600"
        >
          Currently not recording
        </span>
        <span v-else class="text-green-600">
          {{
            formatTimer(replayStore.recorder.recordingSince * 100, false)
          }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss"></style>
