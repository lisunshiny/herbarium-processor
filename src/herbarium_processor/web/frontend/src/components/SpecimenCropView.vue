<template>
  <ImageCropper :imageUrl="image.url" ref="cropper" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import ImageCropper from "@/components/ImageCropper.vue";

const props = defineProps({
  image: { type: Object, required: true }, // {id, url, name, status?, fields?}
});

const cropper = ref(null);
onMounted(async () => {
  // intervalId = setInterval(async () => {
  //   const op = await cropper.value?.getCropOperation();
  //   console.log("[DEBUG crop]", op);
  // }, 1000); // every 10 seconds
});</script>

<style scoped>
.cropper {
  margin: 20px;
}
</style>
