<template>
  <div class="relative w-full h-full bg-base-200 rounded-box overflow-hidden">
    <img
      :src="image_url"
      :alt="specimen.name || 'specimen'"
      draggable="false"
      :style="imageStyle"
      @load="onLoad"
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
*[draggable="false"] {
  -webkit-user-drag: none;
  user-select: none;
}
</style>
