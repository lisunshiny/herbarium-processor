<template>
  <div class="p-8 h-full relative">
    <Cropper
      ref="cropper"
      class="cropper h-full"
      :src="specimen.image_info.url"
      :default-size="defaultSize"
      image-restriction="fit-area"
    />

    <!-- Rotate buttons -->
    <div class="absolute top-4 right-4 flex gap-3">
      <button
        class="btn bg-base-100 btn-sm btn-circle"
        aria-label="Rotate left"
        @click="rotate(-90)"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-rotate-ccw-icon lucide-rotate-ccw"
        >
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
          <path d="M3 3v5h5" />
        </svg>
      </button>
      <button
        class="btn bg-base-100 btn-sm btn-circle"
        aria-label="Rotate right"
        @click="rotate(90)"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-rotate-cw-icon lucide-rotate-cw"
        >
          <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8" />
          <path d="M21 3v5h-5" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { Cropper } from "vue-advanced-cropper";

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  specimen: { type: Object, required: true }, // {id, url, name, status?, fields?}
});

const cropper = ref(null);

function rotate(angle) {
  if (!cropper.value) return;
  cropper.value.rotate(angle);
  cropper.value.refresh();
  // cropper.value.reset();
}

function defaultSize(image) {
  return {
    width: image.imageSize.width,
    height: image.imageSize.height,
  };
}

/**
 * Public method for parent
 */
async function getCropOperation() {
  const res = cropper.value?.getResult();
  if (!res || !res.coordinates) return null;
  const { left, top, width, height } = res.coordinates;
  return {
    x: left,
    y: top,
    width,
    height,
    rotate: res.imageTransforms?.rotate ?? 0,
  };
}

// Expose method so parent can call via ref
defineExpose({ getCropOperation });
</script>

<style scoped></style>
