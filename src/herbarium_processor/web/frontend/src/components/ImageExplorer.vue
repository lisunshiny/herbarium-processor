<template>
  <div
    ref="containerRef"
    class="relative w-full h-full bg-base-200 overflow-hidden"
  >
    <img
      ref="imgRef"
      :src="imageUrl"
      :alt="specimen.name || 'specimen'"
      class="absolute inset-0 m-auto max-w-full max-h-full object-contain block"
    >
    <div class="absolute top-2 right-2 z-10 flex flex-col gap-2">
      <button
        class="btn bg-base-100 btn-md btn-circle"
        @click="zoomIn"
      >
        +
      </button>
      <button
        class="btn bg-base-100 btn-md btn-circle"
        @click="zoomOut"
      >
        -
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import Panzoom from "@panzoom/panzoom";

const props = defineProps({
  specimen: { type: Object, required: true }, // {id, url, name, status?, fields?, image_info: {url}}
  // the url to use, not necessarily specimen.image_info.url
  imageUrl: { type: String, required: true },
});

const specimen = props.specimen;

const containerRef = ref(null);
const imgRef = ref(null);
let panzoomInstance;

const zoomIn = () => panzoomInstance?.zoomIn();
const zoomOut = () => panzoomInstance?.zoomOut();

onMounted(() => {
  panzoomInstance = Panzoom(imgRef.value, {
    maxScale: 5,
    minScale: -2,
  });
  containerRef.value.addEventListener("wheel", panzoomInstance.zoomWithWheel);
});

onBeforeUnmount(() => {
  if (panzoomInstance) {
    containerRef.value.removeEventListener("wheel", panzoomInstance.zoomWithWheel);
    panzoomInstance.destroy();
    panzoomInstance = null;
  }
});
</script>

<style scoped>
</style>
