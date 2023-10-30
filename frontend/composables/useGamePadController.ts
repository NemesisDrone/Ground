import { ref } from 'vue'
import { useDroneComponentsStore } from '~/store/components'

/**
 * This is a composable function that will be used to get and saved the gamepad controls
 * Only one controller can be used by the composables
 */
export const useGamepadController = () => {
  const droneComponentsStore = useDroneComponentsStore()
  const controllerId = ref<null | number>(null)

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
      controllerId.value = e.gamepad.index
    },
    false
  )

  window.addEventListener('gamepaddisconnected', (e) => {
    console.log(
      'Gamepad disconnected from index %d: %s',
      e.gamepad.index,
      e.gamepad.id
    )
    controllerId.value = null
  })

  let lastRoll = 0
  let lastPitch = 0

  const controllerGetValueInterval = setInterval(() => {
    if (controllerId.value != null) {
      const gamepad = navigator.getGamepads()[controllerId.value]
      if (gamepad) {
        let roll = gamepad.axes[0]
        let pitch = gamepad.axes[5]

        if (roll < 0.01 && roll > -0.01) roll = 0
        if (pitch < 0.01 && pitch > -0.01) pitch = 0

        if (roll !== lastRoll || pitch !== lastPitch) {
          droneComponentsStore.websocket?.send({
            route: 'controller',
            data: {
              roll,
              pitch
            }
          })
        }

        lastRoll = roll
        lastPitch = pitch
      } else {
        controllerId.value = null
      }
    }
  }, 150)

  return {
    controllerId,
    controllerGetValueInterval
  }
}
