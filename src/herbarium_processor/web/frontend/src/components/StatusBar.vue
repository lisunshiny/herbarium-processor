<template>
  <AppBar :sticky="true" :progress-percent="progressPercent" />
</template>

<script setup>
import { ref, onMounted, computed, inject } from "vue";
import { useBatchStore } from "@/stores/batch";
import AppBar from "@/components/layout/AppBar.vue";

const props = defineProps({
  id: { type: [String, Number], default: null },
});

const batchStore = useBatchStore();
const specimens = ref([]);
const loading = ref(true);
const error = ref(null);
const progressPercent = inject('progressPercent')

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
