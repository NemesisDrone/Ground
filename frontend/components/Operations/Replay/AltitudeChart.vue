<script setup lang="ts">
let chartComponent = shallowRef<null | Component>(null)
onMounted(async () => {
  chartComponent.value = (await import('vue3-apexcharts')).default
})

const series = {
  series: [{ name: 'Altitude', data: [0, 0, 5, 0, 0, 0, 0] }]
}
const chartOptions = computed(() => ({
  labels: ['0.0s', '0.5s', '0.7s'],
  chart: {
    toolbar: { show: false },
    zoom: { enabled: false },
    type: 'area',
    offsetX: -10
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    dashArray: [0, 12],
    width: [4, 3]
  },
  legend: {
    show: false
  },
  colors: ['#22C55E', '#0ff0ff'],
  markers: {
    size: 0,
    hover: {
      size: 5
    }
  },
  xaxis: {
    labels: {
      style: {
        colors: '#f2f2f2',
        fontSize: '1rem',
        fontFamily: 'Montserrat, Helvetica, Arial, serif'
      }
    },
    axisTicks: {
      show: false
    },
    categories: [],
    axisBorder: {
      show: false
    },
    tickPlacement: 'on'
  },
  yaxis: {
    tickAmount: 5,
    labels: {
      style: {
        colors: '#f2f2f2',
        fontSize: '1rem',
        fontFamily: 'Montserrat, Helvetica, Arial, serif'
      },
      formatter(val: number) {
        return `${val} m`
      }
    }
  },
  grid: {
    borderColor: '#f2f2f2',
    padding: {
      top: -20,
      bottom: -10,
      left: 20
    }
  },
  tooltip: {
    x: { show: false }
  }
}))
</script>

<template>
  <div class="rounded bg-neutral-900 p-4 h-full">
    <component
      :is="chartComponent"
      height="auto"
      type="line"
      :options="chartOptions"
      :series="series.series"
    />
  </div>
</template>

<style lang="css">
.apexcharts-tooltip span {
  color: #171717;
}
</style>
