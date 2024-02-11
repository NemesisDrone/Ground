<script lang="ts" setup>
import ReplayMap from '~/components/Operations/Replay/ReplayMap.vue'
import { useReplayStore } from '~/store/replayStore'
import {
  Play,
  Pause,
  Ban,
  Clock10,
  PauseCircle,
  RotateCcw,
  Aperture,
  Undo2,
  FilePenLine
} from 'lucide-vue-next'
import { formatTimer } from '~/helpers/utils'
import AltitudeChart from '~/components/Operations/Replay/AltitudeChart.vue'
import SpeedChart from '~/components/Operations/Replay/SpeedChart.vue'
import SessionSettings from '~/components/Operations/Replay/SessionSettings.vue'

const replayStore = useReplayStore()

const play = () => {
  // If there is no frames, then don't play
  if (replayStore.frames.length === 0) return
  replayStore.isPlaying = true

  // If the frame is the last one, then reset it to the first frame
  if (replayStore.lastFrameIndex === replayStore.frames.length - 1) {
    replayStore.lastFrameIndex = -1
    replayStore.currentTime = replayStore.frames[0].index
  }

  // Set the current time to the first one if it's not set
  if (replayStore.currentTime === -1) {
    replayStore.currentTime = replayStore.frames[0].index
  }
}

/*
Get the nearest frame index to the current time
Udate the drone position, the drone direction, the drone model position, the drone model rotation
 to the matched time
 */
const updateReplay = () => {
  const currentFrameIndex = replayStore.frames.findIndex(
    (frame) => frame.index === replayStore.currentTime
  )

  if (!currentFrameIndex) return
  replayStore.lastFrameIndex = currentFrameIndex

  replayStore.currentFrame = replayStore.frames[currentFrameIndex]
}

const pause = () => {
  replayStore.isPlaying = false
  console.log('paused')
}

const selectedIntervalReplayMultiple = ref(1)
// When the page is unmounted, we stop the interval
const continueInterval = ref(true)

/**
 * The next function is used to update the current time if the replay is playing
 * We use a setTimeout to call the function every 100ms and to be able to change the interval
 */
const updateIntervalFunction = () => {
  if (!continueInterval.value) return
  setTimeout(
    updateIntervalFunction,
    100 / selectedIntervalReplayMultiple.value
  )
  if (!replayStore.isPlaying) return
  if (replayStore.lastFrameIndex === replayStore.frames.length - 1) {
    replayStore.isPlaying = false
    return
  }

  // Update the current time
  replayStore.currentTime += 10
  sliderTime.value = [replayStore.currentTime]
}
setTimeout(
  updateIntervalFunction,
  100 / selectedIntervalReplayMultiple.value
)

const eventKeyboard = (e: KeyboardEvent) => {
  if (e.code === 'Space') {
    if (replayStore.isPlaying) {
      pause()
    } else {
      play()
    }
  }
}

onMounted(() => {
  if (replayStore.frames.length === 0) return
  replayStore.currentTime = replayStore.frames[0].index
  replayStore.lastFrameIndex = -1
  replayStore.isPlaying = false

  // Add space listener to play/pause on space
  window.addEventListener('keydown', eventKeyboard)
})

onUnmounted(() => {
  continueInterval.value = false

  window.removeEventListener('keydown', eventKeyboard)
})

/*
The sliderTime is used to update the current time when the user change the slider
sliderTime is also updated when the current time is updated by the interval
sliderTime value is an array because the slider component need an array
 */
const sliderTime = ref([0])
watch(
  () => sliderTime.value,
  () => {
    replayStore.currentTime = sliderTime.value[0]
    updateReplay()
  }
)

const isReplayEnd = computed(() => {
  return (
    replayStore.lastFrameIndex === replayStore.frames.length - 1 &&
    !replayStore.isPlaying
  )
})
</script>
<template>
  <div class="w-full h-[100vh]">
    <div class="h-full w-full flex">
      <div class="w-3/5">
        <div class="h-5/6">
          <ReplayMap v-if="replayStore.frames.length > 0" />
        </div>
        <div class="h-1/6 w-full flex flex-col gap-4 p-4">
          <div class="mt-5">
            <UiSlider
              v-model="sliderTime"
              v-if="replayStore.frames.length > 0"
              :max="
                replayStore.frames[replayStore.frames.length - 1].index
              "
              :min="replayStore.frames[0].index"
              :step="10"
            />
          </div>
          <div class="w-full flex gap-2">
            <div
              class="rounded bg-neutral-900 items-center justify-center hover:bg-neutral-800 cursor-pointer"
              @click="replayStore.isDialogSessionsOpen = true"
            >
              <Undo2 :size="22" class="m-2" />
            </div>
            <SessionSettings />
            <div
              v-if="replayStore.frames.length > 0"
              class="rounded bg-neutral-900 flex p-2 items-center"
            >
              <Clock10 :size="18" class="mr-2" />
              <div>
                {{ formatTimer(replayStore.currentTime) }} /
                {{
                  formatTimer(
                    replayStore.frames[replayStore.frames.length - 1].index
                  )
                }}
              </div>
            </div>
            <div
              class="rounded bg-neutral-900 items-center justify-center hover:bg-neutral-800 cursor-pointer"
              @click="replayStore.isPlaying ? pause() : play()"
            >
              <Play
                v-if="!replayStore.isPlaying && !isReplayEnd"
                :size="22"
                class="m-2"
              />
              <RotateCcw
                v-if="!replayStore.isPlaying && isReplayEnd"
                :size="22"
                class="m-2"
              />
              <Pause v-if="replayStore.isPlaying" :size="22" class="m-2" />
            </div>
            <div
              class="rounded bg-neutral-900 flex gap-2 items-center p-2"
            >
              <span
                v-for="multiple in [0.5, 1, 2, 4]"
                class="cursor-pointer hover:text-primary"
                :class="{
                  'text-primary':
                    selectedIntervalReplayMultiple === multiple
                }"
                @click="selectedIntervalReplayMultiple = multiple"
              >
                {{ multiple }}x
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="w-2/5 h-full p-4 flex flex-col gap-4">
        <div>
          <AltitudeChart />
        </div>
        <div>
          <SpeedChart />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss"></style>
