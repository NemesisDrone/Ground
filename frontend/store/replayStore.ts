import { defineStore, acceptHMRUpdate } from 'pinia'
import {
  ReplaySessionData,
  ReplaySession,
  ListingReplaySession
} from '~/types/replay.types'

const initialFrame: ReplaySessionData = {
  id: 0,
  index: 0,
  speed: 0,
  latitude: 0,
  longitude: 0,
  altitude: 0,
  roll: 0,
  pitch: 0,
  yaw: 0
}

export const useReplayStore = defineStore('replay', {
  state: () => ({
    isDialogSessionsOpen: false,
    sessions: [] as ListingReplaySession[],
    currentSession: null as null | ReplaySession,

    isPlaying: false,
    currentTime: -1,
    lastFrameIndex: -1,
    currentFrame: initialFrame
  }),
  getters: {
    frames: (state) => {
      if (!state.currentSession) {
        return []
      }
      return state.currentSession.data
    }
  },

  actions: {
    /*
     * Load all the sessions for listing, without the data
     */
    async getSessions() {
      const { data } = await useHttp().get<ListingReplaySession[]>(
        '/api/replay/sessions/'
      )
      this.sessions = data
    },

    /*
     * Load a session with the data from the backend
     */
    async loadSession(id: number) {
      const { data } = await useHttp().get<ReplaySession>(
        `/api/replay/sessions/${id}/`
      )
      this.currentSession = data

      if (this.currentSession.data.length > 0) {
        this.currentFrame = this.currentSession.data[0]
      }
    },

    /*
     * Delete a session
     */
    async deleteSession(id: number) {
      await useHttp().delete(`/api/replay/sessions/${id}/`)
    },

    /*
     * Update session name
     */
    async updateSessionName(id: number, name: string) {
      await useHttp().patch(`/api/replay/sessions/${id}/`, {
        name
      })
    }
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useReplayStore, import.meta.hot))
}
