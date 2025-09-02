<!-- src/components/BottomBar.vue -->
<template>
  <div
    class="progress-footer px-6 py-2 bg-base-100/95 backdrop-blur border-t border-base-300 bottom-0 w-full z-30"
  >
    <div class="flex justify-between items-center">
        <div>
          <slot name="left" />
        </div>
        <div>
          <slot name="right" />
        </div>
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

// Keep counts reactive to store changes
const states = computed(() => batchStore.getItemsInEachState(props.id));

onMounted(async () => {
  try {
    const batch = await batchStore.getBatch(props.id);
    specimens.value = batch.specimens ?? [];
  } catch (err) {
    error.value = err?.message || "Unknown error";
  } finally {
    loading.value = false;
  }
});
</script>
