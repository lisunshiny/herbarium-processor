<template>
  <div class="relative w-full h-full bg-base-200 overflow-hidden ">
    <img
      :src="image_url"
      :alt="specimen.name || 'specimen'"
      class="absolute inset-0 m-auto max-w-full max-h-full object-contain block"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from "vue";

const props = defineProps({
  specimen: { type: Object, required: true }, // {id, url, name, status?, fields?, image_info: {url}}
  // the url to use, not necessarily specimen.image_info.url
  image_url: { type: String, required: true },
});

const specimen = props.specimen;
</script>

<style scoped>
</style>
