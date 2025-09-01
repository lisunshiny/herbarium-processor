<template>
  <div class="progress-header px-6 py-2 bg-info-content">
    <div class="flex justify-between items-center">
      <span class="text-gray-400">Step 1: Crop</span>
      <span class="font-semibold">5/10</span>
    </div>
  </div>

  <div class="p-6">
    <div v-if="loading">Loading batch…</div>
    <div v-else-if="error" class="text-red-500">
      Failed to load batch: {{ error }}
    </div>
    <div v-else>
      <BaseCard class="max-w-5xl mx-auto">
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
          <aside class="w-64 text-sm text-gray-300">
            <h2 class="font-semibold mb-2">Instructions</h2>
            <ul class="space-y-2 list-disc list-inside">
              <li>Drag the handles to fit the label tightly.</li>
              <li>blah blah.</li>
              <li>
                Press <kbd class="px-1 py-0.5 bg-gray-700 rounded">N</kbd> for
                next.
              </li>
            </ul>
          </aside>
        </div>

        <template #actions>
          <button
            class="btn btn-primary"
            :disabled="isUploading"
            @click="handleUpload"
          >
            <span
              v-if="isUploading"
              class="loading loading-spinner mr-2"
            ></span>
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
    if (batchStore.getBatchState(props.id) !== "cropping") {
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
