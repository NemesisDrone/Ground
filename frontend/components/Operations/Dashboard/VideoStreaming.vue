<script setup lang="ts">
import { ScreenShare, XCircle } from 'lucide-vue-next'
import { storeToRefs } from 'pinia'
import { useSensorsStore } from '~/store/sensors'
import { useNvsStore } from '~/store/nvs'

const route = useRoute()
const sensorsStore = useSensorsStore()
const nvsStore = useNvsStore()


const openInNewTab = () => {
  window.open('/fullscreen/video', '_blank')
}

const closeWindow = () => {
  window.close()
}

const paint = (
  has_image: bool,
  x: number,
  y: number,
  r: number,
  src,
  canvas
) => {
  return

  const ctx = canvas.getContext("2d")
  if (!ctx) {
    return
  }

  const shc = "black"
  const shw = 8
  const fgc = "#20B256"
  const fgw = 2
  const bgc = "#171717"

  const size = Math.min(canvas.clientHeight, canvas.clientWidth)
  const dx = (canvas.clientWidth - size) / 2
  const dy = (canvas.clientHeight - size) / 2

  //context.clearRect(0, 0, size, size);

  if (has_image) {
    let img = new Image(size, size)
    img.src = src;
    ctx.drawImage(img, dx, dy, size, size)
  } else {
    ctx.fillStyle = bgc
    ctx.fillRect(dx, dy, size, size)
  }

  const begin = size / 5
  const axis_len = begin * 3

  ctx.strokeStyle = fgc
  ctx.lineWidth = fgw
  ctx.fillStyle = fgc
  ctx.font = "bold 12px monospace"

  let x_offset = begin * (x % 1)
  let y_offset = begin * (y % 1)

  // X axis
  ctx.strokeStyle = shc
  ctx.lineWidth = shw
  ctx.beginPath()
  ctx.moveTo(dx + begin, dy + size - 10)
  ctx.lineTo(dx + begin + axis_len, dy + size - 10)
  ctx.stroke()

  ctx.strokeStyle = fgc
  ctx.lineWidth = fgw
  ctx.beginPath()
  ctx.moveTo(dx + begin, dy + size - 10)
  ctx.lineTo(dx + begin + axis_len, dy + size - 10)
  ctx.stroke()

  // Y axis
  ctx.strokeStyle = shc
  ctx.lineWidth = shw
  ctx.beginPath()
  ctx.moveTo(dx + 10, dy + begin)
  ctx.lineTo(dx + 10, dy + begin + axis_len)
  ctx.stroke()

  ctx.strokeStyle = fgc
  ctx.lineWidth = fgw
  ctx.beginPath()
  ctx.moveTo(dx + 10, dy + begin)
  ctx.lineTo(dx + 10, dy + begin + axis_len)
  ctx.stroke()

  const x_pos = dx + x_offset + begin;
  let value = Math.floor(x) - 2;
  for (let i = x % 1 < -0.4 ? 1 : 0; i < 3 + (x % 1 > 0.4 ? 0 : 1); i++) {
    let text = value.toFixed(2)

    ctx.shadowColor = shc
    ctx.shadowBlur = shw
    ctx.fillText(text, x_pos + begin * i + 4, dy + size - 14)
    ctx.shadowBlur = 0
    ctx.fillText(text, x_pos + begin * i + 4, dy + size - 14)

    ctx.strokeStyle = shc
    ctx.lineWidth = shw
    ctx.beginPath()
    ctx.moveTo(x_pos + begin * i, dy + size - 10)
    ctx.lineTo(x_pos + begin * i, dy + size - 20)
    ctx.stroke()

    ctx.strokeStyle = fgc
    ctx.lineWidth = fgw
    ctx.beginPath()
    ctx.moveTo(x_pos + begin * i, dy + size - 10)
    ctx.lineTo(x_pos + begin * i, dy + size - 20)
    ctx.stroke()
    value++
  }

  const y_pos = dy + begin + y_offset;
  value = Math.floor(y) - 2;
  for (let i = y % 1 < -0.2 ? 1 : 0; i < 3 + (y % 1 > 0.2 ? 0 : 1); i++) {
    let text = value.toFixed(2);

    ctx.shadowColor = shc
    ctx.shadowBlur = shw
    ctx.fillText(text, dx + 14, y_pos + begin * i - 4)
    ctx.shadowBlur = 0
    ctx.fillText(text, dx + 14, y_pos + begin * i - 4)

    ctx.strokeStyle = shc
    ctx.lineWidth = shw
    ctx.beginPath()
    ctx.moveTo(dx + 10, y_pos + begin * i)
    ctx.lineTo(dx + 20, y_pos + begin * i)
    ctx.stroke()

    ctx.strokeStyle = fgc
    ctx.lineWidth = fgw
    ctx.beginPath()
    ctx.moveTo(dx + 10, y_pos + begin * i)
    ctx.lineTo(dx + 20, y_pos + begin * i)
    ctx.stroke()
    value++
  }

  // Draw roll.
  const radius = 50
  const r_x = dx + size - radius - ctx.measureText("-000.00").width
  const r_y = dy + 25 + radius

  // Arc first.
  ctx.strokeStyle = shc
  ctx.lineWidth = shw
  ctx.beginPath()
  ctx.arc(r_x, r_y, radius, Math.PI * 1.01, Math.PI * -0.01, false)
  ctx.stroke()

  ctx.strokeStyle = fgc
  ctx.lineWidth = fgw
  ctx.beginPath()
  ctx.arc(r_x, r_y, radius, Math.PI * 1.01, Math.PI * -0.01, false)
  ctx.stroke()

  // Draw values
  const floored = Math.floor(r)
  const a_offset = r % 5
  value = floored - (floored % 5) - 15 + (floored % 5 >= 0 ? 5 : 0)
  for (let i = floored % 5 ? 0 : 1; i < 5 + (floored % 5 ? 0 : 1); i++) {
    let text = value.toFixed(2)

    const rad =
      (((value - floored + 15) * 6 - a_offset - 180) * Math.PI) / 180
    const s = Math.sin(rad)
    const c = Math.cos(rad)
    const up = s * (radius + 23)
    const left = c * (radius + 23)

    ctx.shadowColor = shc
    ctx.shadowBlur = shw
    ctx.fillText(
      text,
      r_x + left -
        (left >= (radius + 23) / 2
          ? 16
          : ctx.measureText(text).width - 16),
      r_y + up + (up < (radius + 23) / 7 ? 10 : -16)
    )
    ctx.shadowBlur = 0
    ctx.fillText(
      text,
      r_x + left -
        (left >= (radius + 23) / 2
          ? 16
          : ctx.measureText(text).width - 16),
      r_y + up + (up < (radius + 23) / 7 ? 10 : -16)
    )

    ctx.strokeStyle = shc
    ctx.lineWidth = shw
    ctx.beginPath()
    if (value % 45 == 0) {
      ctx.moveTo(
        r_x + (c * 4 * radius) / 10,
        r_y + (s * 4 * radius) / 10
      );
    } else if (value % 10 == 0) {
      ctx.moveTo(
        r_x + (c * 6 * radius) / 10,
        r_y + (s * 6 * radius) / 10
      );
    } else {
      ctx.moveTo(
        r_x + (c * 8 * radius) / 10,
        r_y + (s * 8 * radius) / 10
      )
    }
    ctx.lineTo(r_x + c * radius, r_y + s * radius)
    ctx.stroke()

    ctx.strokeStyle = fgc
    ctx.lineWidth = fgw
    ctx.beginPath()
    if (value%45 == 0) {
      ctx.moveTo(
        r_x + (c * 4 * radius) / 10,
        r_y + (s * 4 * radius) / 10
      )
    } else if (value%10 == 0) {
      ctx.moveTo(
        r_x + (c * 6 * radius) / 10,
        r_y + (s * 6 * radius) / 10
      )
    } else {
      ctx.moveTo(
        r_x + (c * 8 * radius) / 10,
        r_y + (s * 8 * radius) / 10
      )
    }
    ctx.lineTo(r_x + c * radius, r_y + s * radius)
    ctx.stroke()
    value += 5
  }
}

onMounted(() => {
  let yaw = 0.0
  let pitch = 0.0
  let roll = 0.0

  useNvsWebsocket()
  nvsStore.streamWebsocket.addEventListener('message', event => {
    event.data.arrayBuffer().then(res => {
      document.querySelector("#imager").src = (window.URL || window.webkitURL).createObjectURL(new Blob([new Uint8Array(res)], { type: 'image/jpeg' }))
    });
  });
})

</script>

<template>
  <div class="relative h-full m-0 p-0 overflow-hidden">
    <img class="w-full object-cover h-full m-auto" id="imager"/>
    <canvas class="w-full object-cover h-full m-auto" id="drawing"></canvas>
    <button
      class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
      v-if="route.path !== '/fullscreen/video'"
      @click="openInNewTab"
      title="Open in new tab"
    >
      <ScreenShare :size="24" />
    </button>
    <button
      class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
      v-else
      @click="closeWindow"
      title="Close window"
    >
      <XCircle :size="32" />
    </button>
  </div>
</template>

<style scoped lang="scss"></style>