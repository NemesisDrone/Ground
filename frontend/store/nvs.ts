import { defineStore, acceptHMRUpdate } from 'pinia'

interface State {
  streamWebsocket: WebSocket | null
}

export const useNvsStore = defineStore('nvs', {
  state: (): State => ({
    streamWebsocket: null
  })
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useNvsStore, import.meta.hot)
  )
}
