import { ref } from 'vue'
import { useComponentsStore } from '~/store/components'
import { ComponentsState } from '~/types/components.types'

/**
 * This is a composable function that will be used to get and saved the gamepad controls
 * Only one controller can be used by the composables
 */
export const useGamepadController = () => {
  const componentsStore = useComponentsStore()

  /**
   * When a gamepad is connected, we save the id of the gamepad in the store
   */
  window.addEventListener(
    'gamepadconnected',
    (e) => {
      console.log(
        'Gamepad connected at index %d: %s. %d buttons, %d axes.',
        e.gamepad.index,
        e.gamepad.id,
        e.gamepad.buttons.length,
        e.gamepad.axes.length
      )
      componentsStore.controller.controllerId = e.gamepad.index
      componentsStore.controller.status = ComponentsState.RUNNING
    },
    false
  )

  /**
   * When a gamepad is disconnected, we remove the id of the gamepad in the store
   */
  window.addEventListener('gamepaddisconnected', (e) => {
    console.log(
      'Gamepad disconnected from index %d: %s',
      e.gamepad.index,
      e.gamepad.id
    )
    componentsStore.controller.controllerId = null
    componentsStore.controller.status = ComponentsState.STOPPED
  })

  let lastRoll = 0
  let lastPitch = 0
  /**
   * This interval will be used to get the value of the gamepad axes
   * And send them to the server by websocket
   */
  const controllerGetAxesInterval = setInterval(() => {
    if (componentsStore.controller.controllerId != null) {
      const gamepad =
        navigator.getGamepads()[componentsStore.controller.controllerId]
      if (gamepad) {
        let roll = gamepad.axes[0]
        let pitch = gamepad.axes[5]

        if (roll < 0.01 && roll > -0.01) roll = 0
        if (pitch < 0.01 && pitch > -0.01) pitch = 0

        if (roll !== lastRoll || pitch !== lastPitch) {
          componentsStore.communicationWebsocket?.send({
            route: 'controller',
            data: {
              roll,
              pitch
            }
          })

          componentsStore.controller.axes.roll = roll
          componentsStore.controller.axes.pitch = pitch
        }

        lastRoll = roll
        lastPitch = pitch
      } else {
        componentsStore.controller.controllerId = null
      }
    }
  }, 150)

  let lastDownShift = false
  let lastUpShift = false
  let lastUpHighShift = false
  let lastDownHighShift = false
  /**
   * This interval will be used to get the value of the gamepad buttons
   * And send the new propulsion speed to the server by websocket/other data
   */
  const controllerGetButtonsInterval = setInterval(() => {
    if (componentsStore.controller.controllerId != null) {
      const gamepad =
        navigator.getGamepads()[componentsStore.controller.controllerId]
      if (gamepad) {
        let upShift = gamepad.buttons[7].pressed
        let upHighShift = gamepad.buttons[5].pressed
        let downShift = gamepad.buttons[6].pressed
        let downHighShift = gamepad.buttons[4].pressed
        let propulsionSpeed = componentsStore.propulsionController.speed

        if (lastUpShift != upShift && upShift) {
          propulsionSpeed += 10
          if (propulsionSpeed > 100) propulsionSpeed = 100
        } else if (lastDownShift != downShift && downShift) {
          propulsionSpeed -= 10
          if (propulsionSpeed < 0) propulsionSpeed = 0
        }

        if (lastUpHighShift != upHighShift && upHighShift) {
          propulsionSpeed += 20
          if (propulsionSpeed > 100) propulsionSpeed = 100
        } else if (lastDownHighShift != downHighShift && downHighShift) {
          propulsionSpeed -= 20
          if (propulsionSpeed < 0) propulsionSpeed = 0
        }

        if (
          propulsionSpeed !== componentsStore.propulsionController.speed
        ) {
          componentsStore.communicationWebsocket?.send({
            route: 'propulsion',
            data: {
              speed: propulsionSpeed
            }
          })

          componentsStore.propulsionController.speed = propulsionSpeed
        }

        lastUpShift = upShift
        lastDownShift = downShift
        lastDownHighShift = downHighShift
        lastUpHighShift = upHighShift
      } else {
        componentsStore.controller.controllerId = null
      }
    }
  }, 10)

  return {
    controllerGetAxesInterval,
    controllerGetButtonsInterval
  }
}
