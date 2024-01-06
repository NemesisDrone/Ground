<script setup lang="ts">
import { ScreenShare, XCircle } from 'lucide-vue-next'

const route = useRoute()

const openInNewTab = () => {
  window.open('/fullscreen/video', '_blank')
}

const closeWindow = () => {
  window.close()
}

const paint = (showMessage: bool, has_image: bool, x: number, y: number, r: number, src, canvas) => {
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    console.log("Failed to get context!");
    return;
  }

  const size = Math.min(canvas.clientHeight, canvas.clientWidth);
  const dx = (canvas.clientWidth - size)/2;
  const dy = (canvas.clientHeight - size)/2;
  console.log(size);
  if (showMessage) {
    ctx.fillStyle = "blue";
    ctx.font = "bold 20px serif";
    ctx.fillText("No video available.", dx, 20);
    ctx.stroke();
    return;
  }

  if (has_image) {
    let img = new Image(size, size);
    img.src = src;
  } else {
    ctx.fillStyle = "grey";
    ctx.fillRect(dx, dy, size, size);
  }

  //ctx.drawImage(img,

  const begin = size/5;
  const axis_len = begin * 3;

  ctx.strokeStyle = "red";
  ctx.lineWidth = 2;
  ctx.fillStyle = "red";
  ctx.font = "bold 12px serif"; // Beware that roll numbers drawing depends on this on a constant manner.

  let x_offset = begin * (x%1);
  let y_offset = begin * (y%1);

  // X axis
  ctx.beginPath();
  ctx.moveTo(dx + begin, dy + size - 10);
  ctx.lineTo(dx + begin + axis_len, dy + size - 10);
  ctx.stroke();

  // Y axis
  ctx.beginPath();
  ctx.moveTo(dx + 10, dy + begin);
  ctx.lineTo(dx + 10, dy + begin + axis_len);
  ctx.stroke();

  const x_pos = dx + x_offset + begin;
  let value = Math.floor(x)-2;
  for (let i = (x%1 < -0.4 ? 1 : 0); i < (3 + (x%1 > 0.4 ? 0 : 1)); i++) {
    let text = value.toFixed(2);

    ctx.fillText(text, x_pos + begin*i +4, dy + size - 14);
    ctx.beginPath();
    ctx.moveTo(x_pos + begin*i, dy + size - 10);
    ctx.lineTo(x_pos + begin*i, dy + size - 20);
    ctx.stroke();
    value++;
  }

  const y_pos = dy + begin + y_offset;
  value = Math.floor(y)-2;
  for (let i = (y%1 < -0.2 ? 1 : 0); i < (3 + (y%1 > 0.2 ? 0 : 1)); i++) {
    let text = value.toFixed(2);

    ctx.fillText(text, dx + 14, y_pos + begin*i - 4);
    ctx.beginPath();
    ctx.moveTo(dx + 10, y_pos + begin*i);
    ctx.lineTo(dx + 20, y_pos + begin*i);
    ctx.stroke();
    value++;
  }

  // Draw roll.
  const radius = 50;
  const r_x = dx + size - 20 - radius - 22;
  const r_y = dy + 25 + radius;

  // Arc first.
  ctx.beginPath();
  ctx.arc(r_x, r_y, radius, Math.PI * 1.01, Math.PI * -0.01, false);
  ctx.stroke();

  // Draw values
  const floored = Math.floor(r);
  const a_offset = r%5;
  value = (floored - floored%5)-15 + (floored%5 >= 0 ? 5 : 0);
  console.log(r%5);
  for (let i = (floored%5 ? 0 : 1); i < (5 + (floored%5 ? 0 : 1)); i++) {
    let text = value.toFixed(2);
    console.log(i.toString() + ", " + text);

    const rad = ((value - floored + 15) * 7 - a_offset - 180)*Math.PI/180;
    const s = Math.sin(rad);
    const c = Math.cos(rad);
    const up = s * (radius+23);
    const left = c * (radius+23);

    ctx.fillText(text, r_x + left - (left >= 0 ? 16 : 9 * ((floored%100 ? 3 : (floored%10 ? 2 : (floored != 0 ? 1 : 0)))) + (floored < 0 ? 1 : 0)), r_y + up + (up < (radius+23)/7 ? 10 : -16));
    ctx.beginPath();
    if (value%45 == 0) {
      ctx.moveTo(r_x + c*(4*radius/10), r_y + s*(4*radius/10));
    } else if (value%10 == 0) {
      ctx.moveTo(r_x + c*(6*radius/10), r_y + s*(6*radius/10));
    } else {
      ctx.moveTo(r_x + c*(8*radius/10), r_y + s*(8*radius/10));
    }
    ctx.lineTo(r_x + c*(radius), r_y + s*(radius));
    ctx.stroke();
    value += 5;
  }
}

onMounted(() => {
  const canvas = document.querySelector("#imager");

  function ws_connect() {
    let ws = new WebSocket(
      useRuntimeConfig().public.NVS_WEB_SOCKET_URL as string
    );

    ws.addEventListener("error", event => {
      console.error("WS ERROR: ", event.message);
      ws.close();
      ws = null;
    });

    ws.addEventListener("close", event => {
      ws.close();
      ws = null;
    });

    ws.addEventListener('message', event => {
      event.data.arrayBuffer().then(res => {
        let blob = new Blob([new Uint8Array(res)], {type: "image/jpeg"});
        paint(false, true, -0.2, 2.1, 0.0, (window.URL || window.webkitURL).createObjectURL(blob), canvas);
      });
    });
  };

  addEventListener("resize", (event) => {
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
  });

  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;
  ws_connect();

  // Dummy. [TODO] Remove it once properly settled.
  let w = 0.0;
  setInterval(() => {
    w += 0.005;
    let c = Math.cos(w);
    paint(false, false, c*10, c*(-20), c * 360, "", canvas);
  }, 100);
})

</script>

<template>
  <div class="relative h-full m-0 p-0 overflow-hidden">
    <canvas class="w-full object-cover h-full m-auto" id="imager"></canvas>
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
