import {useNvsStore} from '~/store/nvs'

/**
 * Create a new WebSocket instance
 * and provide it to the whole application
 * Add callbacks to handle incoming messages
 */
export const useNvsWebsocket = () => {
  const nvsStore = useNvsStore()
console.log("here")
  let ws = new WebSocket(
    useRuntimeConfig().public.NVS_WEB_SOCKET_URL as string
  )

  ws.addEventListener("error", event => {
    console.error("WS ERROR: ", event.message)
    ws.close()
    ws = null
  });

  ws.addEventListener("close", event => {
    ws.close()
    ws = null
  });

  nvsStore.streamWebsocket = ws

  const close = () => {
    ws.close()
    nvsStore.streamWebsocket = null
  }

  return { ws, close }
}
