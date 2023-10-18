import { defineStore, acceptHMRUpdate } from 'pinia'
import { LogLine } from '~/types/logs.types'

interface State {
  logs: LogLine[]
}

export const useLogsStore = defineStore('logs', {
  state: (): State => ({
    logs: []
  })
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useLogsStore, import.meta.hot))
}
