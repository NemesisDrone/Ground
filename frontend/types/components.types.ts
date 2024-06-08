export enum ComponentsState {
  STARTED = 'STARTED',
  STOPPED = 'STOPPED',
  NOT_EXPECTED = 'NOT_EXPECTED'
}

export interface DroneComponent {
  status: ComponentsState
  name: string
  description: string
  disableActions?: boolean
  routeSlug?: string
  [key: string]: any
}
