<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue' // Import ref from Vue
import { ScrollArea } from '@/components/ui/scroll-area'
import { useLogsStore } from '~/store/logs'
import { storeToRefs } from 'pinia'
import { LogLevels } from '~/types/logs.types'

const logsStore = useLogsStore()
const { logs } = storeToRefs(logsStore)
</script>

<template>
  <div class="rounded-md bg-neutral-900 h-full p-2">
    <ScrollArea
      class="h-full rounded bg-black p-3 overflow-y-auto"
      ref="scrollAreaRef"
      :scroll-to-bottom="true"
    >
      <div v-for="(log, i) in logs" :key="i">
        <div class="flex gap-1.5">
          <div
            class="w-2 min-w-[0.5rem] h-2 rounded-full mt-1.5"
            :class="{
              'bg-gray-500': log.level === LogLevels.DEBUG,
              'bg-blue-500': log.level === LogLevels.INFO,
              'bg-orange-500': log.level === LogLevels.WARNING,
              'bg-red-500': log.level === LogLevels.ERROR,
              'bg-red-900': log.level === LogLevels.CRITICAL
            }"
          ></div>
          <div class="text-sm text-neutral-100">{{ log.level }}</div>
          <div class="text-sm text-neutral-100">{{ log.time }}</div>
          <div class="text-sm text-neutral-100">{{ log.message }}</div>
        </div>
      </div>
    </ScrollArea>
  </div>
</template>

<style scoped lang="scss"></style>
