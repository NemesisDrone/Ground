<script setup lang="ts">
import {
  AlertTriangle,
  MonitorCheck,
  MonitorX,
  Power,
  PowerOff,
  RotateCcw
} from 'lucide-vue-next'
import { ComponentsState, DroneComponent } from '~/types/components.types'
import {
  Popover,
  PopoverContent,
  PopoverTrigger
} from '~/components/ui/popover'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger
} from '~/components/ui/tooltip'
import { Separator } from '~/components/ui/separator'
import { useComponentsStore } from '~/store/components'

const componentsStore = useComponentsStore()

const props = defineProps<{
  component: DroneComponent
  // Sry for the any, but I don't know how to type this, that's why I'm using typescript. I promise. I know i shoud look into the LucideIcon docs and find out how to type this. But I'm lazy. And I'm not getting paid for this. So I'm not gonna do it. I'm sorry. I'm not sorry.
  icon?: any
}>()

const isPopoverOpen = ref(false)
const openStateChanged = (isOpen: boolean) => {
  isPopoverOpen.value = isOpen
}

const colorFromStatus = computed(() => {
  let borderClass = ''
  switch (props.component.status) {
    case ComponentsState.STOPPED:
      borderClass = 'border-red-600 hover:border-red-900'
      break
    case ComponentsState.ERROR:
      borderClass = 'border-orange-600 hover:border-orange-900'
      break
    case ComponentsState.RUNNING:
      borderClass = 'border-green-600 hover:border-green-900'
      break
  }

  return [
    borderClass,
    isPopoverOpen.value ? `bg-neutral-800` : `bg-neutral-900`
  ].join(' ')
})

const TextColorFromStatus = computed(() => {
  switch (props.component.status) {
    case ComponentsState.STOPPED:
      return 'text-red-600'
    case ComponentsState.ERROR:
      return 'text-orange-600'
    case ComponentsState.RUNNING:
      return 'text-green-600'
  }
})

const IconFromStatus = computed(() => {
  switch (props.component.status) {
    case ComponentsState.STOPPED:
      return MonitorX
    case ComponentsState.ERROR:
      return AlertTriangle
    case ComponentsState.RUNNING:
      return MonitorCheck
  }
})

// watch for changes in websocket
watch(
  () => componentsStore.communicationWebsocket,
  () => {
    if (props.component.routeSlug) {
      componentsStore.communicationWebsocket?.onMessage(
        [
          `state:${props.component.routeSlug}:started`,
          `state:${props.component.routeSlug}:running`
        ],
        (event: any) => {
          props.component.status = ComponentsState.RUNNING
        }
      )

      componentsStore.communicationWebsocket?.onMessage(
        [`state:${props.component.routeSlug}:stopped`],
        (event: any) => {
          props.component.status = ComponentsState.STOPPED
        }
      )
    }
  }
)

const startComponent = () => {
  componentsStore.communicationWebsocket?.send({
    route: `state:start:${props.component.routeSlug}`,
    data: {
      component: props.component.routeSlug
    }
  })
}

const stopComponent = () => {
  componentsStore.communicationWebsocket?.send({
    route: `state:stop:${props.component.routeSlug}`,
    data: {
      component: props.component.routeSlug
    }
  })
}

const restartComponent = () => {
  componentsStore.communicationWebsocket?.send({
    route: `state:restart:${props.component.routeSlug}`,
    data: {
      component: props.component.routeSlug
    }
  })
}
</script>

<template>
  <Popover @update:open="openStateChanged">
    <PopoverTrigger as-child>
      <div
        :class="`border-2 rounded flex flex-col justify-center items-center cursor-pointer ${colorFromStatus}`"
      >
        <component
          :is="props.icon ? props.icon : IconFromStatus"
          :class="TextColorFromStatus"
        />

        <div
          class="text-center text-sm font-bold"
          :class="TextColorFromStatus"
        >
          {{ component.name }}
        </div>
      </div>
    </PopoverTrigger>
    <PopoverContent
      class="w-80"
      side="top"
      @interact-outside="openStateChanged(false)"
    >
      <div class="flex justify-between">
        <div class="space-y-2">
          <h4 class="font-medium leading-none">
            {{ component.description }}
          </h4>
          <p
            v-if="!props.component.disableActions"
            class="text-sm text-muted-foreground"
          >
            Actions
          </p>
        </div>
        <div class="flex flex-col justify-center items-center">
          <component :is="IconFromStatus" :class="TextColorFromStatus" />

          <div
            class="text-center text-sm font-bold"
            :class="TextColorFromStatus"
          >
            {{
              props.component.status === ComponentsState.STOPPED
                ? 'Stopped'
                : props.component.status === ComponentsState.ERROR
                ? 'Error'
                : 'Running'
            }}
          </div>
        </div>
      </div>
      <div
        v-if="!props.component.disableActions"
        class="flex h-10 items-center space-x-4 text-sm mt-4"
      >
        <template
          v-if="props.component.status === ComponentsState.STOPPED"
        >
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger as-child>
                <Power
                  :size="32"
                  class="text-primary cursor-pointer"
                  @click="startComponent"
                />
              </TooltipTrigger>
              <TooltipContent>
                <p>Power on component {{ props.component.description }}</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </template>
        <template
          v-else-if="
            props.component.status === ComponentsState.RUNNING ||
            props.component.status === ComponentsState.ERROR
          "
        >
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger as-child>
                <PowerOff
                  :size="32"
                  class="text-red-600 cursor-pointer"
                  @click="stopComponent"
                />
              </TooltipTrigger>
              <TooltipContent>
                <p>
                  Power off component {{ props.component.description }}
                </p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <Separator orientation="vertical" />

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger as-child>
                <RotateCcw
                  :size="32"
                  class="text-primary cursor-pointer"
                  @click="restartComponent"
                />
              </TooltipTrigger>
              <TooltipContent>
                <p>Restart component {{ props.component.description }}</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </template>
      </div>
    </PopoverContent>
  </Popover>
</template>

<style scoped lang="scss"></style>
