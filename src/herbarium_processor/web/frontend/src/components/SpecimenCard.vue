<template>
    <div class="card card-border bg-base-100 mx-4 my-8">
    <div class="card-body">

  I am a specimen cards
  <img v-if="specimen.image_info.url" :src="specimen.image_info.url" class="w-full h-40 object-cover" />
  <div class="p-2 text-sm">
    {{ specimen.image_info.name || specimen.image_info.id }}
  </div>
</div>
</div>
</template>

<script setup>
const props = defineProps({
  specimen: { type: Object, required: true }, // {id, url, name, status?, fields?}
});
</script>

<style scoped>
/* ... */
</style>
