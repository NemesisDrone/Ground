interface Canal {
  canal: number
  gpios: number[]
}

export interface Model {
  id: number
  brushless_canals: Canal[]
  servo_canals: Canal[]
  name: string
  drone_settings: number // The id of the drone settings that this model belongs to
}
