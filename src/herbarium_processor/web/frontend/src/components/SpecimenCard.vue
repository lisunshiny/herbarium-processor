<template>
    <div class="card card-border bg-base-100 mx-4 my-8">
    <div class="card-body">

  I am a specimen cards
  <img v-if="image.url" :src="image.url" class="w-full h-40 object-cover" />
  <div class="p-2 text-sm">
    {{ image.filename || image.id }}
  </div>
</div>
</div>
</template>

<script setup>
const props = defineProps({
  image: { type: Object, required: true }, // {id, url, name, status?, fields?}
});
</script>

<style scoped>
/* ... */
</style>
