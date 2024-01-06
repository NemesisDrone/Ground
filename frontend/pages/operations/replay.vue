<script lang="ts" setup>
import ReplayMap from '~/components/Operations/Replay/ReplayMap.vue'
import { useReplayStore } from '~/store/replayStore'
import { Play, PauseCircle, Ban } from 'lucide-vue-next'
definePageMeta({
  layout: 'sidebar',
  keepalive: false
})
useHead({
  title: 'Replay'
})

const replayStore = useReplayStore()

const play = () => {
  // If there is no frames, then don't play
  if (replayStore.frames.length === 0) return
  replayStore.isPlaying = true

  // If the frame is the last one, then reset it to the first frame
  if (replayStore.lastFrameIndex === replayStore.frames.length - 1) {
    replayStore.lastFrameIndex = -1
    replayStore.currentTimeStamp = -1
  }

  // Set the current timestamp to the first one if it's not set
  if (replayStore.currentTimeStamp === -1) {
    replayStore.currentTimeStamp = replayStore.frames[0].timestamp
  }
}

/*
 * Watch the current timestamp and update everything related to the replay
 * When the current timestamp is updated, we call the updateReplay function
 */
watch(
  () => replayStore.currentTimeStamp,
  () => {
    if (!replayStore.isPlaying) return

    updateReplay()
  }
)
/*
Get the nearest frame index to the current timestamp
Udate the drone position, the drone direction, the drone model position, the drone model rotation
 to the matched timestamp
 */
const updateReplay = () => {
  const frameIndex = replayStore.getNearestFrameIndex(
    replayStore.currentTimeStamp
  )

  // If there is no new frame, don't update
  if (frameIndex === replayStore.lastFrameIndex) return

  // Update the last frame index
  replayStore.lastFrameIndex = frameIndex
  replayStore.currentFrame = replayStore.frames[frameIndex]

  console.log(replayStore.frames[frameIndex])
}

const pause = () => {
  replayStore.isPlaying = false
  console.log('paused')
}

const stop = () => {
  replayStore.isPlaying = false
  replayStore.currentTimeStamp = -1
  replayStore.lastFrameIndex = -1
  console.log('stopped')
}

/**
 * The next interval is used to update the current timestamp if the replay is playing
 */
const playingInterval = setInterval(() => {
  if (!replayStore.isPlaying) return

  if (replayStore.lastFrameIndex === replayStore.frames.length - 1) {
    replayStore.isPlaying = false
    return
  }

  // Update the current timestamp
  replayStore.currentTimeStamp += 100
}, 100)

onUnmounted(() => {
  // Clear the interval when the component is unmounted
  clearInterval(playingInterval)
})

onMounted(() => {
  replayStore.currentTimeStamp = -1
  replayStore.lastFrameIndex = -1
  replayStore.isPlaying = false
})
</script>
<template>
  <div class="w-full h-[100vh]">
    <div class="h-5/6 w-full flex gap-4">
      <div class="w-3/5">
        <ReplayMap />
      </div>
      <div class="w-2/5">Other</div>
    </div>
    <div class="h-1/6 w-full flex gap-4">
      <div class="w-4/5 bg-red-500 h-full"></div>
      <div class="w-1/5 h-full">
        <div class="flex gap-2">
          <UiButton @click="play">
            <Play :size="18" class="mr-2" />
            Play
          </UiButton>
          <UiButton variant="destructive" @click="pause">
            <PauseCircle :size="18" class="mr-2" />
            Pause
          </UiButton>
          <UiButton @click="stop">
            <Ban :size="18" class="mr-2" />
            Stop
          </UiButton>
        </div>
        {{ replayStore.isPlaying ? 'Playing' : 'Not playing' }}
      </div>
    </div>
  </div>
</template>

<style lang="scss"></style>
