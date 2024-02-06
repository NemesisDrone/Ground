<script setup lang="ts">
import { useReplayStore } from '~/store/replayStore'
import { ListingReplaySession, ReplaySession } from '~/types/replay.types'
import Overlay from '~/components/ui/overlay/Overlay.vue'
import { Trash } from 'lucide-vue-next'
import {
  formatTime,
  getDurationBetweenTimestampsFormat
} from '~/helpers/utils'

const replayStore = useReplayStore()
const isLoading = ref(false)
const searchString = ref('')
const selectedSession = ref<ListingReplaySession | null>(null)

const sessions = computed(() => {
  if (searchString.value === '') return replayStore.sessions
  return replayStore.sessions.filter((session) =>
    session.name.toLowerCase().includes(searchString.value.toLowerCase())
  )
})

const selectSession = async (session: ListingReplaySession) => {
  isLoading.value = true
  await replayStore.loadSession(session.id)
  isLoading.value = false

  replayStore.isDialogSessionsOpen = false
}

const deleteSession = async (session: ListingReplaySession) => {
  isLoading.value = true

  await replayStore.deleteSession(session.id)
  await replayStore.getSessions()

  isLoading.value = false
}
</script>

<template>
  <UiDialog
    :open="replayStore.isDialogSessionsOpen"
    @update:open="replayStore.isDialogSessionsOpen = $event"
  >
    <UiDialogContent>
      <UiDialogHeader>
        <UiDialogTitle> Select a session</UiDialogTitle>
      </UiDialogHeader>
      <Overlay :show="isLoading">
        <UiInput
          v-model="searchString"
          placeholder="Search"
          class="mb-4"
        />
        <UiScrollArea style="height: 300px">
          <UiTable class="w-full">
            <UiTableHeader>
              <UiTableRow>
                <UiTableHead> Name</UiTableHead>
                <UiTableHead> Date</UiTableHead>
                <UiTableHead> Duration</UiTableHead>
                <UiTableHead> Action</UiTableHead>
              </UiTableRow>
            </UiTableHeader>
            <UiTableBody>
              <UiTableRow
                v-for="session in sessions"
                :key="session.id"
                class="cursor-pointer"
                :class="{
                  'bg-neutral-800': selectedSession?.id === session.id
                }"
                @click="selectedSession = session"
                @dblclick="selectSession(session)"
              >
                <UiTableCell> {{ session.name }}</UiTableCell>
                <UiTableCell>
                  {{ formatTime(session.start_time) }}
                </UiTableCell>
                <UiTableCell>
                  {{
                    getDurationBetweenTimestampsFormat(
                      session.start_time,
                      session.end_time
                    )
                  }}
                </UiTableCell>
                <UiTableCell>
                  <UiDialog>
                    <UiDialogTrigger>
                      <Trash :size="18" class="m-2 text-red-600" />
                    </UiDialogTrigger>
                    <UiDialogContent>
                      <UiDialogHeader>
                        <UiDialogTitle>
                          Are you sure you want to delete this session?
                        </UiDialogTitle>
                      </UiDialogHeader>
                      <UiDialogFooter>
                        <UiDialogClose as-child>
                          <UiButton
                            type="button"
                            variant="destructive"
                            @click="deleteSession(session)"
                          >
                            Delete
                          </UiButton>
                        </UiDialogClose>
                      </UiDialogFooter>
                    </UiDialogContent>
                  </UiDialog>
                </UiTableCell>
              </UiTableRow>
              <UiTableRow v-if="sessions.length === 0" class="text-center">
                <UiTableCell colspan="4"> No sessions found</UiTableCell>
              </UiTableRow>
            </UiTableBody>
          </UiTable>
        </UiScrollArea>
        <UiDialogFooter>
          <UiButton
            :disabled="selectedSession === null"
            @click="selectSession(selectedSession as ListingReplaySession)"
          >
            Select
          </UiButton>
        </UiDialogFooter>
      </Overlay>
    </UiDialogContent>
  </UiDialog>
</template>

<style scoped lang="scss"></style>
