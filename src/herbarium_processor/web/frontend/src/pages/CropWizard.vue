<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">CROP Batch {{ id }}</h1>

    <div v-if="loading">Loading batch…</div>
    <div v-else-if="error" class="text-red-500">
      Failed to load batch: {{ error }}
    </div>
    <div v-else>
<BaseCard class="m-4 mx-auto">
  <!-- Constrain height and width -->
  <div class="flex gap-6">
    <!-- Left: crop views, scrollable if tall -->
    <div class="flex-1 overflow-y-auto max-h-[70vh] pr-2">
      <SpecimenCropView
        v-for="img in images"
        :key="img.id"
        :image="img"
        class="mb-4"
      />
    </div>

    <!-- Right: instructions, fixed narrow width -->
    <div class="w-64 text-sm text-gray-600">
      <h2 class="font-semibold mb-2">Instructions</h2>
      <p>
        Lorem ipsum add some instructions about cropping here. Explain to the
        user how to align, zoom, and confirm the crop before moving to the next
        image.
      </p>
    </div>
  </div>

  <template #actions>
    <button
      class="btn btn-primary"
      :disabled="isUploading"
      @click="handleUpload"
    >
      <span v-if="isUploading" class="loading loading-spinner mr-2"></span>
      {{ isUploading ? "Uploading…" : "Process label & next" }}
    </button>
  </template>
</BaseCard>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import SpecimenCropView from "@/components/SpecimenCropView.vue";
import { useBatchStore } from "@/stores/batch"; // our Pinia store
import BaseCard from "@/components/ui/BaseCard.vue";

const props = defineProps({
  id: { type: String, required: true },
});

const images = ref([]);
const loading = ref(true);
const error = ref(null);

const batchStore = useBatchStore();

onMounted(async () => {
  try {
    const batch = await batchStore.getBatch(props.id); // use store
    if (batchStore.getBatchState(props.id) !== "crop") {
      throw new Error("not at crop");
    }
    images.value = batch.images ?? [];
  } catch (err) {
    error.value = err.message || "Unknown error";
  } finally {
    loading.value = false;
  }
});
</script>
