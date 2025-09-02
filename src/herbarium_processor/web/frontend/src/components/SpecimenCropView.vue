<template>
  <div class="p-8 h-full">
    <Cropper
      ref="cropper"
      class="cropper"
      :src="specimen.image_info.url"
      :default-size="defaultSize"
      image-restriction="fit-area"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Cropper } from "vue-advanced-cropper";

const props = defineProps({
  specimen: { type: Object, required: true }, // {id, url, name, status?, fields?}
});

console.log(props.specimen);
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
    x: left,
    y: top,
    width,
    height,
    rotate: res.angle ?? 0,
  };
}

// Expose method so parent can call via ref
defineExpose({ getCropOperation });
</script>

<style scoped>
</style>
