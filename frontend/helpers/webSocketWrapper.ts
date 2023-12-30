import { useUserStore } from '~/store/user'

/**
 * A wrapper around the WebSocket class that allows for adding and removing listeners
 * for specific message types.
 * @param url The url to connect to.
 */
class WebSocketWrapper {
  private socket: WebSocket
  private listeners: Record<string, ((data: any) => void)[]> = {}

  constructor(url: string) {
    const userStore = useUserStore()
    // not good but nevermind
    url =
      url +
      '?access=' +
      userStore.accessToken +
      '&refresh=' +
      userStore.refreshToken
    this.socket = new WebSocket(url)

    this.socket.onmessage = (event) => {
      this.handleMessage(JSON.parse(event.data))
    }
  }

  public onMessage(
    types: string | string[],
    callback: (data: any) => void
  ) {
    if (!Array.isArray(types)) {
      types = [types]
    }
    types.forEach((type) => {
      if (!this.listeners[type]) {
        this.listeners[type] = []
      }
      this.listeners[type].push(callback)
    })
  }

  public removeListener(type: string, callback: (data: any) => void) {
    const typeListeners = this.listeners[type]
    if (typeListeners) {
      const index = typeListeners.indexOf(callback)
      if (index !== -1) {
        typeListeners.splice(index, 1)
      }
    }
  }

  private handleMessage(message: any) {
    if (message.type && this.listeners[message.type]) {
      this.listeners[message.type].forEach((callback) => {
        callback(message)
      })
    }
  }

  public send(message: any) {
    this.socket.send(JSON.stringify(message))
  }

  public close() {
    this.socket.close()
  }
}

export { WebSocketWrapper }
