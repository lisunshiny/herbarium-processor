<template>
  <div class="cropper-wrapper">
    <Cropper
      ref="cropper"
      class="cropper"
      :src="props.imageUrl"
      :default-size="defaultSize"
      image-restriction="fit-area"
    />
  </div>
</template>

<script setup>
const props = defineProps({
  imageUrl: { type: String, required: true },
});

// import component + stylesheet
import { ref } from "vue";
import { Cropper } from "vue-advanced-cropper";

const cropper = ref(null);

function defaultSize(image) {
  return {
    width: image.imageSize.width,
    height: image.imageSize.height
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
    left,
    top,
    width,
    height,
  };
}

// Expose method so parent can call via ref
defineExpose({ getCropOperation });
</script>

<style scoped></style>
