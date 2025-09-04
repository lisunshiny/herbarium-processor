<template>
  <div
    class="progress-header px-6 py-2 bg-base-100 border-y border-base-300 top-0 sticky z-30"
  >
    <div class="flex justify-between items-center">
      <a href="/" class="text-xl cursor-pointer">🌿 Parsely</a>
      <div class="breadcrumbs text-sm">
        <ul>
          <li>Prepare</li>
          <li>Validate</li>
          <li>Export</li>
        </ul>
      </div>

      <!-- <div claass="flex flex-wrap items-center gap-2">
        <span
          class="inline-flex items-center gap-1 rounded-full bg-neutral/10 text-neutral px-2.5 py-0.5 text-xs font-medium cursor-default"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-neutral"></span> Crop
          <span class="opacity-60">({{ states.cropping }})</span>
        </span>
        <span
          class="inline-flex items-center gap-1 rounded-full bg-primary/10 text-primary px-2.5 py-0.5 text-xs font-medium cursor-default"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-primary"></span> Parse
          <span class="opacity-60">({{ states.digitizing }})</span>
        </span>
        <span
          class="inline-flex items-center gap-1 rounded-full bg-warning/10 text-warning px-2.5 py-0.5 text-xs font-medium cursor-default"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-warning"></span> Needs review
          <span class="opacity-60">({{ states.ready }})</span>
        </span>
        <span
          class="inline-flex items-center gap-1 rounded-full bg-success/10 text-success px-2.5 py-0.5 text-xs font-medium cursor-default"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-success"></span> Ready
          <span class="opacity-60">({{ states.reviewed }})</span>
        </span>
      </div> -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useBatchStore } from "@/stores/batch";

const props = defineProps({
  id: { type: [String, Number], default: null },
});

const batchStore = useBatchStore();
const specimens = ref([]);
const loading = ref(true);
const error = ref(null);

// Make counts reactive to store changes
const states = computed(() => batchStore.getItemsInEachState(props.id));

onMounted(async () => {
  try {
    const batch = await batchStore.getBatch(props.id); // use store
    specimens.value = batch.specimens ?? [];
  } catch (err) {
    error.value = err?.message || "Unknown error";
  } finally {
    loading.value = false;
  }
});
</script>
