<template>
  <WizardLayout :batchId="id">
    <main class="h-full flex-1 overflow-hidden">
      <div v-if="loading" class="h-full grid place-items-center">
        Loading batch…
      </div>

      <div v-else-if="error" class="h-full grid place-items-center text-error">
        Failed to load batch: {{ error }}
      </div>
      <div
        v-else-if="specimens.length === 0"
        class="h-full grid place-items-center text-base-content/60"
      >
        No images in this batch.
      </div>
      <div v-else class="h-full overflow-auto p-4">
        <SpecimenLabelView
          v-if="currentSpecimen"
          :key="currentSpecimen?.image_info?.id ?? currentIndex"
          :specimen="currentSpecimen"
          :batchId="id"
        />
      </div>
    </main>
    <!-- Bottom bar content -->
    <template #bottom-left></template>

    <template #bottom-right>
      <button
        class="btn btn-primary"
        :disabled="!currentSpecimen"
        @click="handleNext"
      >
        {{ currentIndex < specimens.length - 1 ? "Next specimen" : "Finish" }}
      </button>
    </template>
  </WizardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import SpecimenLabelView from "@/components/SpecimenLabelView.vue";
import WizardLayout from "@/components/WizardLayout.vue";
import { useBatchStore } from "@/stores/batch"; // our Pinia store

const props = defineProps({
  id: { type: String, required: true },
});
const router = useRouter();
const specimens = ref([]);
const loading = ref(true);
const error = ref(null);
const currentIndex = ref(0);
const batchStore = useBatchStore();
const hasSpecimens = computed(() => specimens.value.length > 0);
const currentSpecimen = computed(() =>
  hasSpecimens.value ? specimens.value[currentIndex.value] : null
);
const progressText = computed(() =>
  hasSpecimens.value
    ? `${currentIndex.value + 1}/${specimens.value.length}`
    : "0/0"
);
const progressPercent = computed(() =>
  hasSpecimens.value
    ? Math.round(((currentIndex.value + 1) / specimens.value.length) * 100)
    : 0
);

function handleNext() {
  if (currentIndex.value < specimens.value.length - 1) {
    currentIndex.value++;
  } else {
    router.push({ name: "batch", params: { id: props.id } });
  }
}

onMounted(async () => {
  try {
    const batch = await batchStore.getBatch(props.id); // use store
    specimens.value = batch.specimens ?? [];

    // Auto-navigate to CropWizard if the stage is "cropping"
    const stage = batchStore.getBatchState(props.id);
    if (stage === "cropping") {
      router.replace({ name: "cropWizard", params: { id: props.id } });
      return;
    }
  } catch (err) {
    error.value = err.message || "Unknown error";
  } finally {
    loading.value = false;
  }
});
</script>
