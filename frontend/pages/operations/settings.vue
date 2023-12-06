<script setup lang="ts">
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from '@/components/ui/table'
import { Input } from '@/components/ui/input'
definePageMeta({
  layout: 'sidebar'
})

const canals = reactive([
  {
    canal: 1,
    gpios: '1,2'
  },
  {
    canal: 2,
    gpios: '3'
  },
  {
    canal: 3,
    gpios: '4'
  }
])
</script>

<template>
  <div class="p-4">
    <h1 class="text-3xl">Settings</h1>
    <p>Temporary raw settings.</p>
    <Table class="w-[600px] mt-4">
      <TableHeader>
        <TableRow>
          <TableHead>Canal</TableHead>
          <TableHead>GPIOs</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="canal in canals" :key="canal.canal">
          <TableCell>{{ canal.canal }}</TableCell>
          <TableCell><Input v-model="canal.gpios" /></TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>

<style scoped lang="scss"></style>
