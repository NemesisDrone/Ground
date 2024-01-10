import { defineStore, acceptHMRUpdate } from 'pinia'

type ReplayFrame = {
  timestamp: number
  time: number
  gps: {
    lat: number
    lng: number
  }
  altitude: number
  roll: number
  pitch: number
  yaw: number
}

const initialFrame: ReplayFrame = {
  timestamp: 0,
  time: 0,
  gps: {
    lat: -0.7563779,
    lng: 48.0879123
  },
  altitude: 100,
  roll: 0,
  pitch: 0,
  yaw: -90
}

const ct = new Date().getTime()
export const useReplayStore = defineStore('replay', {
  state: () => ({
    isPlaying: false,
    currentTime: -1,
    lastFrameIndex: -1,
    currentFrame: initialFrame,
    frames: [
      {
        timestamp: ct,
        time: 0,
        gps: {
          lat: -0.7563779,
          lng: 48.0879123
        },
        altitude: 100,
        roll: 0,
        pitch: 0,
        yaw: -90
      },
      {
        timestamp: ct + 500,
        time: 500,
        gps: {
          lat: -0.7564779,
          lng: 48.0879123
        },
        altitude: 102,
        roll: 0,
        pitch: 10,
        yaw: -90
      },
      {
        timestamp: ct + 2000,
        time: 2000,
        gps: {
          lat: -0.7565779,
          lng: 48.0879123
        },
        altitude: 105,
        roll: 0,
        pitch: 20,
        yaw: -90
      },

      {
        timestamp: ct + 3000,
        time: 3000,
        gps: {
          lat: -0.7565779,
          lng: 48.0879123
        },
        altitude: 110,
        roll: 0,
        pitch: 20,
        yaw: -90
      },
      {
        timestamp: ct + 3500,
        time: 3500,
        gps: {
          lat: -0.7566779,
          lng: 48.0879123
        },
        altitude: 109,
        roll: 0,
        pitch: 0,
        yaw: -90
      },
      {
        timestamp: ct + 4000,
        time: 4000,
        gps: {
          lat: -0.7567779,
          lng: 48.0879123
        },
        altitude: 112,
        roll: 0,
        pitch: -10,
        yaw: -90
      },
      {
        timestamp: ct + 4600,
        time: 4600,
        gps: {
          lat: -0.7568779,
          lng: 48.0879123
        },
        altitude: 108,
        roll: 0,
        pitch: -10,
        yaw: -90
      },
      {
        timestamp: ct + 5200,
        time: 5200,
        gps: {
          lat: -0.7569779,
          lng: 48.0879123
        },
        altitude: 105,
        roll: 0,
        pitch: -10,
        yaw: -90
      },
      {
        timestamp: ct + 6000,
        time: 6000,
        gps: {
          lat: -0.7570779,
          lng: 48.0879123
        },
        altitude: 100,
        roll: 0,
        pitch: 0,
        yaw: -90
      },
      {
        timestamp: ct + 7000,
        time: 7000,
        gps: {
          lat: -0.7571779,
          lng: 48.0879123
        },
        altitude: 110,
        roll: 0,
        pitch: 30,
        yaw: -90
      },
      {
        timestamp: ct + 8000,
        time: 8000,
        gps: {
          lat: -0.7572779,
          lng: 48.0879123
        },
        altitude: 115,
        roll: 0,
        pitch: 30,
        yaw: -90
      },
      {
        timestamp: ct + 9000,
        time: 9000,
        gps: {
          lat: -0.7573779,
          lng: 48.0879123
        },
        altitude: 120,
        roll: 0,
        pitch: 30,
        yaw: -90
      },
      {
        timestamp: ct + 1000,
        time: 10000,
        gps: {
          lat: -0.7574779,
          lng: 48.0879123
        },
        altitude: 125,
        roll: 0,
        pitch: 30,
        yaw: -90
      },
      {
        timestamp: ct + 11000,
        time: 11000,
        gps: {
          lat: -0.7575779,
          lng: 48.0879123
        },
        altitude: 130,
        roll: 0,
        pitch: 10,
        yaw: -90
      },
      {
        timestamp: ct + 12000,
        time: 12000,
        gps: {
          lat: -0.7576779,
          lng: 48.0879123
        },
        altitude: 135,
        roll: 0,
        pitch: 0,
        yaw: -90
      },
      {
        timestamp: ct + 13000,
        time: 13000,
        gps: {
          lat: -0.7577779,
          lng: 48.0879123
        },
        altitude: 135,
        roll: 0,
        pitch: 0,
        yaw: -90
      }
    ] as ReplayFrame[]
  }),
  getters: {
    getNearestFrameIndex: (state) => (time: number) => {
      let nearest = state.lastFrameIndex

      for (let i = 0; i < state.frames.length; i++) {
        if (state.frames[i].time >= time) {
          break
        }
        nearest = i
      }
      return nearest
    }
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useReplayStore, import.meta.hot))
}
