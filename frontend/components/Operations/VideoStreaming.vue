<script setup lang="ts">
import { ScreenShare, XCircle } from 'lucide-vue-next'

const route = useRoute()

const openInNewTab = () => {
  window.open('/fullscreen/video', '_blank')
}

const closeWindow = () => {
  window.close()
}


const paint = (showMessage: bool, x: number, y: number, src, canvas) => {
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

  let img = new Image(size, size);
  img.src = src;

  //ctx.drawImage(img,

  const begin = size/5;
  const axis_len = begin * 3;

  ctx.fillStyle = "black";
  ctx.font = "bold 9px serif";

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
  for (i = (x%1 < -0.4 ? 1 : 0); i < (3 + (x%1 > 0.4 ? 0 : 1)); i++) {
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
  for (i = (y%1 < -0.2 ? 1 : 0); i < (3 + (y%1 > 0.2 ? 0 : 1)); i++) {
    let text = value.toFixed(2);

    ctx.fillText(text, dx + 14, y_pos + begin*i - 4);
    ctx.beginPath();
    ctx.moveTo(dx + 10, y_pos + begin*i);
    ctx.lineTo(dx + 20, y_pos + begin*i);
    ctx.stroke();
    value++;
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
        paint(false, -0.2, 2.1, (window.URL || window.webkitURL).createObjectURL(blob), canvas);
      });
    });
  };

  ws_connect();
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
