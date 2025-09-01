<template>
  <div class="progress-header px-6 py-2 bg-base-300">
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
              v-if="currentSpecimen"
              :key="currentSpecimen?.id ?? currentIndex"
              :specimen="currentSpecimen"
              :ref="setCropperRef"
              class="mb-4"
            />
          </div>

          <!-- Right: instructions, fixed narrow width -->
          <aside class="w-64 text-sm text-gray-300 border-l border-base-300 pl-4">
            <h2 class="text-lg font-semibold tracking-tight text-base-content">
              Crop · {{ currentSpecimen.image_info.name }}
            </h2>
            <p class="mt-2 text-sm text-base-content/80">
              Draw the crop box around the label. Use the handles to resize.
              Lorem ipsum dolor, sit amet consectetur adipisicing elit. Eum
              perspiciatis totam corporis ratione delectus nisi repellendus
              maxime! Ex magnam exercitationem maxime aut nemo consequuntur
              saepe vero voluptas earum consequatur? Sed.
            </p>

            <p class="mt-3 text-xs leading-snug text-base-content/60">
              Guidelines: include barcode; exclude mounting board edges.
            </p>
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
            {{
              isUploading
                ? "Uploading…"
                : currentIndex < specimens.length - 1
                ? "Process label & next"
                : "Finish & proceed to labeling"
            }}
          </button>
        </template>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  computed,
  onMounted,
  onBeforeUpdate,
  onMounted as vueOnMounted,
  onBeforeUnmount,
} from "vue";
import { useRouter } from "vue-router";
import SpecimenCropView from "@/components/SpecimenCropView.vue";
import { useBatchStore } from "@/stores/batch";
import BaseCard from "@/components/ui/BaseCard.vue";

const props = defineProps({
  id: { type: String, required: true },
});

const router = useRouter();
const specimens = ref([]);
const loading = ref(true);
const error = ref(null);
const cropperRefs = ref([]);
const isUploading = ref(false);
const currentIndex = ref(0);

const batchStore = useBatchStore();

const hasSpecimens = computed(() => specimens.value.length > 0);
const currentSpecimen = computed(() =>
  hasSpecimens.value ? specimens.value[currentIndex.value] : null
);
console.log(currentSpecimen);
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

// Avoid stale element refs between patches
onBeforeUpdate(() => {
  cropperRefs.value = [];
});

onMounted(async () => {
  try {
    const batch = await batchStore.getBatch(props.id); // use store
    if (batchStore.getBatchState(props.id) !== "cropping") {
      router.push({ name: "batch", params: { id: props.id } });
    }
    specimens.value = batch.specimens ?? [];
    cropperRefs.value = Array(specimens.value.length).fill(null); // ensure array length matches specimens
  } catch (err) {
    error.value = err?.message || "Unknown error";
  } finally {
    loading.value = false;
  }
});

// Safe function ref: never use .value from template; set here.
function setCropperRef(el) {
  // Function refs fire with el (instance) on mount and el=null on unmount.
  if (!el) return;
  const i = currentIndex.value;
  if (!Array.isArray(cropperRefs.value)) cropperRefs.value = [];
  // Make sure our array is at least i+1 long
  if (cropperRefs.value.length < i + 1) {
    cropperRefs.value.length = i + 1;
  }
  cropperRefs.value[i] = el;
}

async function handleUpload() {
  if (!hasSpecimens.value) return;
  isUploading.value = true;

  try {
    const specimen = specimens.value[currentIndex.value];
    const cropperRef = cropperRefs.value[currentIndex.value];

    if (!specimen) throw new Error("Missing current image");
    if (!cropperRef || typeof cropperRef.getCropOperation !== "function") {
      throw new Error("Cropper not ready");
    }

    const cropOp = await cropperRef.getCropOperation();
    if (!cropOp) throw new Error("No crop operation");

    // Fire-and-forget via Pinia store; it will merge result into state
    batchStore
      .cropAndInfer(props.id, specimen.id, cropOp)
      .catch((e) => console.error("crop_and_infer error", e));

    // Immediately advance UI without waiting for POST
    if (currentIndex.value < specimens.value.length - 1) {
      currentIndex.value++;
    } else {
      router.push({ name: "batch", params: { id: props.id } });
    }
  } catch (err) {
    error.value = err?.message || "Unknown error";
  } finally {
    // Re-enable the button right away for next interaction
    isUploading.value = false;
  }
}
</script>
