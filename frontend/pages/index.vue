<script lang="ts" setup>
import type { Container } from 'tsparticles-engine'
import { useUserStore } from '~/store/user'
import { storeToRefs } from 'pinia'

const router = useRouter()

const options = {
  fullScreen: {
    zIndex: 0
  },
  particles: {
    number: {
      value: 175,
      density: {
        enable: true,
        value_area: 1000
      }
    },
    move: {
      enable: true,
      speed: 0.5
    },
    color: {
      value: ['#20B256']
    },
    shape: {
      type: 'circle',
      stroke: {
        width: 0,
        color: '#fff'
      },
      polygon: {
        nb_sides: 5
      },
      image: {
        width: 100,
        height: 100
      }
    },
    opacity: {
      value: 0.6,
      random: false,
      anim: {
        enable: false,
        speed: 1,
        opacity_min: 0.1,
        sync: false
      }
    },
    size: {
      value: 2,
      random: true,
      anim: {
        enable: false,
        speed: 40,
        size_min: 0.1,
        sync: false
      }
    },
    line_linked: {
      enable: true,
      distance: 120,
      color: '#ffffff',
      opacity: 0.4,
      width: 1
    }
  },
  interactivity: {
    detect_on: 'canvas',
    events: {
      onhover: {
        enable: true,
        mode: 'grab'
      },
      onclick: {
        enable: false
      },
      resize: true
    },
    modes: {
      grab: {
        distance: 140,
        line_linked: {
          opacity: 1
        }
      },
      bubble: {
        distance: 400,
        size: 40,
        duration: 2,
        opacity: 8,
        speed: 3
      },
      repulse: {
        distance: 200,
        duration: 0.4
      },
      push: {
        particles_nb: 4
      },
      remove: {
        particles_nb: 2
      }
    }
  },
  retina_detect: true
}

const authStore = useUserStore()
const { authenticated } = storeToRefs(authStore)

const user = ref({
  identifier: '',
  password: ''
})
const loginError = ref(false)
const isLoading = ref(false)
const logIn = async () => {
  isLoading.value = true

  await authStore.authenticateUser(user.value)
  if (authenticated.value) {
    router.push('/operations/dashboard')
  } else {
    loginError.value = true
  }

  isLoading.value = false
}

watch(
  user,
  () => {
    loginError.value = false
  },
  { deep: true }
)
</script>

<template>
  <div>
    <NuxtParticles id="tsparticles" :options="options"> </NuxtParticles>

    <div
      class="mx-auto w-full flex flex-col justify-center sm:w-[350px] mt-[5rem] px-4"
    >
      <div class="flex flex-col space-y-2 text-center">
        <h1 class="text-3xl font-semibold tracking-tight z-10">Nemesis</h1>
        <p class="text-sm text-muted-foreground z-10">
          Enter your identifications informations
        </p>
        <p v-if="loginError" class="text-red-600 z-10">
          Invalid credentials
        </p>
      </div>
      <form class="z-10">
        <div class="grid space-y-2 mt-5 z-10">
          <div class="grid space-y-1">
            <UiLabel for="identifier">Identifier</UiLabel>
            <UiInput
              id="identifier"
              placeholder="Enter your identifier"
              autocomplete="off"
              v-model="user.identifier"
            />
          </div>
          <div class="grid space-y-1">
            <UiLabel for="password">Password</UiLabel>
            <UiInput
              id="password"
              placeholder="Enter your password"
              type="password"
              autocomplete="off"
              v-model="user.password"
            />
          </div>
        </div>
        <UiButton
          class="mt-4 z-10 w-full"
          @click="logIn"
          :is-loading="isLoading"
        >
          Connect
        </UiButton>
      </form>
    </div>
  </div>
</template>
