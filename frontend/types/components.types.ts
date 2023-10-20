export enum ComponentsState {
  RUNNING = 'RUNNING',
  STOPPED = 'STOPPED',
  ERROR = 'ERROR'
}

export interface DroneComponent {
  status: ComponentsState
  name: string
  description: string
}
