<script setup lang="ts">
import { LogOut } from 'lucide-vue-next'
import { useUserStore } from '~/store/user'

const isLogOutLoading = ref(false)
const logOut = async () => {
  isLogOutLoading.value = true

  await useUserStore().logOut()
  await useRouter().push('/?disconnected')

  isLogOutLoading.value = false
}
</script>

<template>
  <UiDialog>
    <UiDialogTrigger>
      <UiButton variant="destructive">
        <LogOut :size="18" class="mr-2" />
        Log out
      </UiButton>
    </UiDialogTrigger>
    <UiDialogContent>
      <UiDialogHeader>
        <UiDialogTitle>Log out?</UiDialogTitle>
        <UiDialogDescription>
          You will be logged out. You can log in again.
        </UiDialogDescription>
      </UiDialogHeader>
      <UiDialogFooter>
        <UiButton
          variant="destructive"
          @click="logOut"
          :is-loading="isLogOutLoading"
        >
          Confirm
        </UiButton>
      </UiDialogFooter>
    </UiDialogContent>
  </UiDialog>
</template>

<style scoped lang="scss"></style>
