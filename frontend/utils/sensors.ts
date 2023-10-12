import { BatteryStatus, PropulsorSpeedStatus } from '~/types/sensors.types'

/*
This function is used to get the battery status from the battery Level.
For instance if the battery is at 40%. The status will be BatteryStatus.LOW
*/
export const getBatteryStatus = (batteryLevel: number): BatteryStatus => {
  if (batteryLevel > 85) {
    return BatteryStatus.FULL
  }
  if (batteryLevel > 50) {
    return BatteryStatus.MEDIUM
  }
  if (batteryLevel > 20) {
    return BatteryStatus.LOW
  }
  if (batteryLevel > 5) {
    return BatteryStatus.VERY_LOW
  }
  return BatteryStatus.EMPTY
}

/*
This function is used to get the propulsor speed status from the speed of the brushless motor.
For instance if the speed in percentage of the motor is 60%. Then the status will be PropulsorSpeedStatus.MEDIUM
*/
export const getPropulsorSpeedStatus = (
  propulsorSpeed: number
): PropulsorSpeedStatus => {
  if (propulsorSpeed > 80) {
    return PropulsorSpeedStatus.HIGH
  }
  if (propulsorSpeed > 40) {
    return PropulsorSpeedStatus.MEDIUM
  }
  if (propulsorSpeed > 3) {
    return PropulsorSpeedStatus.LOW
  }
  return PropulsorSpeedStatus.STOPPED
}
