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
    var ws = new WebSocket('ws://10.0.3.1:7000') // [TODO] See what address to use here.
    //ws.binaryType = "arraybuffer";

    ws.addEventListener('error', (event) => {
      console.error('WS ERROR: ', event.message)
      ws.close()
      setTimeout(function () {
        ws_connect()
      }, 500)
    })

    ws.addEventListener('close', (event) => {
      ws.close()
      setTimeout(ws_connect, 500)
    })

    ws.addEventListener('message', (event) => {
      event.data.arrayBuffer().then((res) => {
        var abv = new Uint8Array(res)
        var blob = new Blob([abv], { type: 'image/jpeg' })
        var uc = window.URL || window.webkitURL
        var iu = uc.createObjectURL(blob)
        var i = document.querySelector('#imager')
        i.src = iu
      })
    })

    ws.addEventListener('message', (event) => {
      var abv = new Uint8Array(event.data)
      var blob = new Blob([abv], { type: 'image/jpeg' })
      var uc = window.URL || window.webkitURL
      var iu = uc.createObjectURL(blob)
      var i = document.querySelector('#imager')
      i.src = iu
    })
  }

  // ws_connect();
})
</script>

<template>
  <div class="relative h-full m-0 p-0 overflow-hidden">
    <img class="w-full object-cover h-full" id="imager" />
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
