import { storeToRefs } from 'pinia'
import { useUserStore } from '~/store/user'

/**
 * Route named "index" is the login route
 */
export default defineNuxtRouteMiddleware((to, from) => {
  const userStore = useUserStore()
  const { authenticated, accessToken, refreshToken } =
    storeToRefs(userStore)

  if (accessToken && refreshToken) {
    authenticated.value = true

    // if (to?.name === 'index') {
    //   return navigateTo('/operations/dashboard')
    // }
  }
  userStore.getUserData()

  if ((!accessToken || !refreshToken) && to?.name !== 'index') {
    abortNavigation()
    return navigateTo('/')
  }
})
