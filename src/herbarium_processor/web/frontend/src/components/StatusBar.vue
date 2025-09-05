<template>
  <header class="navbar bg-base-100 top-0 border-y border-base-300 sticky z-30">
    <div class="flex-1">
      <a href="/" class="pl-2 pr-2 text-xl cursor-pointer">🌿 Parsely Studio</a
      ><span
        class="badge badge-outline badge-xs badge-error translate-y-[-2px]"
      >
        Pre-alpha
      </span>
    </div>
    <progress
      v-if="progressPercent !== null"
      class="progress progress-primary absolute bottom-0 left-0 w-full h-1"
      :value="progressPercent"
      max="100"
    />
  </header>
</template>

<script setup>
import { ref, onMounted, computed, inject } from "vue";
import { useBatchStore } from "@/stores/batch";

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
