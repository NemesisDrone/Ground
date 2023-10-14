import { storeToRefs } from 'pinia'
import { useAuthStore } from '~/store/auth'

/**
 * Route named "index" is the login route
 */
export default defineNuxtRouteMiddleware((to, from) => {
  const { authenticated } = storeToRefs(useAuthStore())
  const access = useCookie('access')
  const refresh = useCookie('refresh')

  if (access.value && refresh.value) {
    authenticated.value = true

    // if (to?.name === 'index') {
    //   return navigateTo('/dashboard')
    // }
  }

  if ((!access.value || !refresh.value) && to?.name !== 'index') {
    abortNavigation()
    return navigateTo('/')
  }
})
