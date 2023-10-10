<script lang="ts" setup>
import { useCounterStore } from '~/store/counter'

const counterStore = useCounterStore()
console.log(counterStore.count)
</script>

<template>
  <div class="w-full h-full flex min-h-[100vh]">
    <div class="w-2/3 border p-2 border-sky-500"></div>
    <div class="w-1/3 border p-2 border-red-500">
      <div class="w-full h-1/2 border border-green-500">GPS</div>
      <div class="w-full h-1/2 border border-yellow-500">VIDEO</div>
    </div>
  </div>
</template>

<style lang="scss"></style>
