import { storeToRefs } from 'pinia'
import { useUserStore } from '~/store/user'

/**
 * Route named "index" is the login route
 */
export default defineNuxtRouteMiddleware((to, from) => {
  const userStore = useUserStore()
  const { authenticated } = storeToRefs(userStore)
  const access = useCookie('access')
  const refresh = useCookie('refresh')

  if (access.value && refresh.value) {
    authenticated.value = true

    // if (to?.name === 'index') {
    //   return navigateTo('/dashboard')
    // }
  }
  userStore.getUserData()

  if ((!access.value || !refresh.value) && to?.name !== 'index') {
    abortNavigation()
    return navigateTo('/')
  }
})
