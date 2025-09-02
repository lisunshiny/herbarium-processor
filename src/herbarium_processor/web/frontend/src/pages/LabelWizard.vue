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
      <div v-else class="h-full">
        <div
          v-if="currentSpecimen"
          :key="currentSpecimen?.image_info?.id ?? currentIndex"
          class="mx-auto grid grid-cols-1 md:grid-cols-[1fr_auto] h-full"
        >
          <!-- Left card (stretches) -->
          <ImageExplorer
            :specimen="currentSpecimen"
            :image_url="currentSpecimen.image_info.ocr_bounding_url"
          />

          <!-- Right card (fixed w-64, scrollable) -->
          <div class="w-64 h-full overflow-y-auto border-l border-base-300 p-4">
            <h2>
              Digitized fields
              <div
                v-if="!currentSpecimen.image_info.user_edited_llm_output"
                class="badge badge-xs badge-outline badge-warning"
              >
                Needs review
              </div>
              <div v-else class="badge badge-xs badge-outline badge-success">
                Reviewed
              </div>
            </h2>
            <p
              v-if="!currentSpecimen.image_info.user_edited_llm_output"
              class="text-xs leading-snug text-base-content/60"
            >
              These fields were autocompleted by an AI model and may contain
              errors. Please review and correct before finalizing.
            </p>
            <div
              v-if="!currentSpecimen.image_info.llm_output"
              class="text-sm text-base-content/60"
            >
              No extracted fields yet.
            </div>
            <div v-else>
              <div
                v-for="(val, key) in form"
                :key="key"
                class="form-control mb-3"
              >
                <label class="label py-1">
                  <span class="label-text text-xs">{{ key }}</span>
                </label>
                <textarea
                  v-model="form[key]"
                  rows="1"
                  class="textarea textarea-bordered textarea-sm w-full overflow-hidden max-h-60 [field-sizing:content] min-h-0 py-1"
                >
                </textarea>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    <!-- Bottom bar content -->
    <template #bottom-left></template>

    <template #bottom-right>
      <button class="btn btn-primary" @click="saveLabel">
        <span v-if="!currentSpecimen?.image_info?.user_edited_llm_output"
          >Mark as reviewed</span
        >
        <span v-else>Update</span>
      </button>
      <button class="btn" @click="revert">Revert</button>

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
import { ref, computed, onMounted, reactive, watch } from "vue";
import { useRouter } from "vue-router";
import WizardLayout from "@/components/WizardLayout.vue";
import ImageExplorer from "@/components/ImageExplorer.vue";
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

const form = reactive({
  ...(currentSpecimen.value?.image_info?.llm_output || {}),
});

function setFormFrom(obj) {
  for (const k of Object.keys(form)) {
    if (!(obj && Object.prototype.hasOwnProperty.call(obj, k))) {
      delete form[k];
    }
  }
  if (obj) {
    for (const [k, v] of Object.entries(obj)) {
      form[k] = v;
    }
  }
}

function revert() {
  setFormFrom(currentSpecimen.value?.image_info?.llm_output || {});
}

async function saveLabel() {
  if (!currentSpecimen.value) return;
  const payload = JSON.parse(JSON.stringify(form));
  await batchStore.postUserUpdatedLlmLabels(
    props.id,
    currentSpecimen.value.image_info.id,
    payload
  );
  if (currentIndex.value < specimens.value.length - 1) {
    currentIndex.value++;
  } else {
    router.push({ name: "batch", params: { id: props.id } });
  }
}

watch(
  () => currentSpecimen.value?.image_info?.llm_output,
  (newVal) => setFormFrom(newVal || {}),
  { immediate: true, deep: true }
);

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
