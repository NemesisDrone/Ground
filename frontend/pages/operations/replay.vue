<script lang="ts" setup>
import ReplayMap from '~/components/Operations/Replay/ReplayMap.vue'
import { useReplayStore } from '~/store/replayStore'
import { Ban, Clock10, PauseCircle } from 'lucide-vue-next'

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
    replayStore.currentTime = replayStore.frames[0].time
  }

  // Set the current time to the first one if it's not set
  if (replayStore.currentTime === -1) {
    replayStore.currentTime = replayStore.frames[0].time
  }
}

/*
Get the nearest frame index to the current time
Udate the drone position, the drone direction, the drone model position, the drone model rotation
 to the matched time
 */
const updateReplay = () => {
  const frameIndex = replayStore.getNearestFrameIndex(
    replayStore.currentTime
  )

  // If there is no new frame, don't update
  if (frameIndex === replayStore.lastFrameIndex) return

  // Update the last frame index
  replayStore.lastFrameIndex = frameIndex
  replayStore.currentFrame = replayStore.frames[frameIndex]

  // console.log(replayStore.frames[frameIndex])
}

const pause = () => {
  replayStore.isPlaying = false
  console.log('paused')
}

const stop = () => {
  replayStore.isPlaying = false
  replayStore.currentTime = replayStore.frames[0].time
  replayStore.lastFrameIndex = -1
  console.log('stopped')
}

/**
 * The next interval is used to update the current time if the replay is playing
 */
const playingInterval = setInterval(() => {
  if (!replayStore.isPlaying) return

  if (replayStore.lastFrameIndex === replayStore.frames.length - 1) {
    replayStore.isPlaying = false
    return
  }

  // Update the current time
  replayStore.currentTime += 100
  sliderTime.value = [replayStore.currentTime]
}, 100)

onUnmounted(() => {
  // Clear the interval when the component is unmounted
  clearInterval(playingInterval)
})

onMounted(() => {
  replayStore.currentTime = replayStore.frames[0].time
  replayStore.lastFrameIndex = -1
  replayStore.isPlaying = false
})

const sliderTime = ref([0])
watch(
  () => sliderTime.value,
  () => {
    replayStore.currentTime = sliderTime.value[0]
    updateReplay()
  }
)

const formatTime = (time: number) => {
  let seconds = time / 1000
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  const twoDecimalSeconds = remainingSeconds.toFixed(2).padStart(5, '0')

  return `${String(minutes).padStart(2, '0')}:${twoDecimalSeconds}`
}
</script>
<template>
  <div class="w-full h-[100vh]">
    <div class="h-5/6 w-full flex gap-4">
      <div class="w-3/5">
        <ReplayMap />
      </div>
      <div class="w-2/5">Other</div>
    </div>
    <div class="h-1/6 w-full flex gap-4 p-4">
      <div class="w-4/5 h-full flex flex-col">
        <div class="mt-5">
          <UiSlider
            v-model="sliderTime"
            :max="replayStore.frames[replayStore.frames.length - 1].time"
            :min="replayStore.frames[0].time"
            :step="100"
          />
        </div>
        <div class="w-full mt-4 flex">
          <div class="rounded bg-neutral-900 flex p-2 items-center">
            <Clock10 :size="18" class="mr-2" />
            <div>
              {{ formatTime(replayStore.currentTime) }} /
              {{
                formatTime(
                  replayStore.frames[replayStore.frames.length - 1].time
                )
              }}
            </div>
          </div>
        </div>
      </div>
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
