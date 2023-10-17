<script setup lang="ts">
import { buttonVariants } from '.'
import { cn } from '~/helpers/utils'

interface Props {
  variant?: NonNullable<Parameters<typeof buttonVariants>[0]>['variant']
  size?: NonNullable<Parameters<typeof buttonVariants>[0]>['size']
  as?: string
  isLoading?: boolean
}

withDefaults(defineProps<Props>(), {
  as: 'button'
})
</script>

<template>
  <component
    :is="as"
    :class="cn(buttonVariants({ variant, size }), $attrs.class ?? '')"
    class="relative"
    :disabled="isLoading"
  >
    <div
      v-if="isLoading"
      class="absolute left-4 inline-block h-5 w-5 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
      role="status"
    ></div>
    <slot />
  </component>
</template>
