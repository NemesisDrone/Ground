<script setup lang="ts">
import { useReplayStore } from '~/store/replayStore'

let chartComponent = shallowRef<null | Component>(null)
onMounted(async () => {
  chartComponent.value = (await import('vue3-apexcharts')).default
})

const replayStore = useReplayStore()

const altitudeData = computed(() => {
  const series = [
    { name: 'Altitude by frame', data: [] as number[] },
    { name: 'Altitude', data: [] as number[] }
  ]
  const labels: string[] = []

  // if true then we had the altitude in 'Altitude by frame'
  let addInAltitudeByFrame = true
  replayStore.frames.forEach((frame, index) => {
    series[1].data.push(frame.altitude)

    if (addInAltitudeByFrame) {
      series[0].data.push(frame.altitude)
      if (index === replayStore.lastFrameIndex)
        addInAltitudeByFrame = false
    }

    labels.push(`${Math.round((frame.time / 1000) * 100) / 100}s`)
  })

  return {
    series,
    labels
  }
})

const chartOptions = computed(() => ({
  labels: altitudeData.value.labels,
  chart: {
    toolbar: { show: false },
    zoom: { enabled: false },
    type: 'line',
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
  colors: ['#71FFA5', '#ebe9f1'],
  fill: {
    type: 'gradient',
    gradient: {
      shade: 'dark',
      inverseColors: false,
      gradientToColors: ['#22C55E', '#ebe9f1'],
      shadeIntensity: 1,
      type: 'horizontal',
      opacityFrom: 1,
      opacityTo: 1,
      stops: [0, 100, 100, 100]
    }
  },
  markers: {
    size: 0,
    hover: {
      size: 5
    }
  },
  xaxis: {
    labels: {
      show: false,
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
      top: -10
      // bottom: -10
      // left: 20
    }
  },
  tooltip: {
    x: { show: false }
  }
}))
</script>

<template>
  <div class="rounded bg-neutral-900 h-full p-4">
    <component
      :is="chartComponent"
      height="auto"
      type="line"
      :options="chartOptions"
      :series="altitudeData.series"
    />
  </div>
</template>

<style lang="css">
.apexcharts-tooltip span {
  color: #171717;
}
</style>
