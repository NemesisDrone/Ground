<script setup lang="ts">
import { ScreenShare, XCircle } from 'lucide-vue-next'

const route = useRoute()

const openInNewTab = () => {
  window.open('/fullscreen/video', '_blank')
}

const closeWindow = () => {
  window.close()
}

onMounted(() => {
      function ws_connect() {
        let ws = new WebSocket('ws://100.87.214.117:7000'); // [TODO] See what address to use here.

        ws.addEventListener("error", event => {
          console.error("WS ERROR: ", event.message);
          ws.close();
          ws = null;
          setTimeout(function() {
            ws_connect();
          }, 500);
        });

        ws.addEventListener("close", event => {
          ws.close();
          ws = null;
          setTimeout(ws_connect, 500);
        });

        ws.addEventListener('message', event => {
          event.data.arrayBuffer().then(res => {
            document.querySelector("#imager").src = (window.URL || window.webkitURL).createObjectURL(new Blob([new Uint8Array(res)], {type: "image/jpeg"}));
          });
        });
      };

      ws_connect();
})

</script>

<template>
  <div class="relative h-full m-0 p-0 overflow-hidden">
    <div class="nvs-container">
        <img
            class="w-full object-cover h-full"
            id="imager"
        />
        <p class="nvs-message">Stream unavailable.</p>
    </div>
    <button
      class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
      v-if="route.path !== '/fullscreen/video'"
      @click="openInNewTab"
    >
      <ScreenShare :size="24" />
    </button>
    <button
      class="absolute top-0 right-0 z-50 bg-neutral-900 rounded p-1.5 mt-2.5 mr-2.5 text-primary"
      v-else
      @click="closeWindow"
    >
      <XCircle :size="32" />
    </button>
  </div>
</template>

<style scoped lang="scss"></style>
