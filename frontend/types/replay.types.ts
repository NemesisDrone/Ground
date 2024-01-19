export interface ReplaySessionData {
  id: number
  index: number
  speed: number
  latitude: number
  longitude: number
  altitude: number
  roll: number
  pitch: number
  yaw: number
}

export interface ListingReplaySession {
  id: number
  name: string
  start_time: number
  end_time: number
}

export interface ReplaySession extends ListingReplaySession {
  data: ReplaySessionData[]
}
