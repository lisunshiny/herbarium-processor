<template>
  <div class="m-4 mt-8 space-y-4 max-w-4xl mx-auto">
    <div
      class="mx-4 rounded-lg bg-gradient-to-r from-blue-500 to-info to text-white py-3 px-6 text-center shadow-md"
    >
      <span class="font-bold"> 👋🏼 New here?</span> Parsely Studio turns specimen
      labels into digital records in 4 quick steps —
      <a
        href="/how-it-works"
        class="underline font-medium hover:text-green-100"
      >
        see how it works</a>.
    </div>
    <BaseCard class="mx-4">
      <template #header>
        Upload photos of specimens
      </template>
      <!-- Drop zone -->
      <div
        :class="[
          'border-2 border-dashed rounded p-12 text-center cursor-pointer',
          isDragging ? 'border-primary bg-base-200' : 'border-base-300',
        ]"
        @click="triggerFileSelect"
        @dragover.prevent="onDragEnter"
        @dragenter.prevent="onDragEnter"
        @dragleave.prevent="onDragLeave"
        @drop.prevent="onDrop"
      >
        <p>Drag & drop up to 10 images, or click to select</p>
      </div>

      <!-- Hidden file input -->
      <input
        ref="fileInput"
        type="file"
        multiple
        accept="image/*"
        class="hidden"
        @change="onFileSelect"
      >

      <!-- Thumbnails -->
      <div
        v-if="uploads.length"
        class="flex flex-wrap gap-4 mt-4"
      >
        <div
          v-for="(upload, index) in uploads"
          :key="index"
          class="relative w-24 h-24"
        >
          <img
            :src="upload.url"
            alt="preview"
            class="object-cover w-full h-full rounded"
          >
          <button
            type="button"
            class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center"
            @click="removeImage(index)"
          >
            &times;
          </button>
        </div>
      </div>
      <div class="collapse collapse-plus bg-base-200">
        <input
          type="checkbox"
          class="peer"
        >
        <div class="collapse-title font-medium text-base-content">
          Advanced settings
        </div>
        <div class="collapse-content text-sm text-base-content/80 space-y-3">
          <label class="label cursor-pointer justify-start gap-3 p-0">
            <input
              v-model="skipCrop"
              type="checkbox"
              class="checkbox checkbox-primary"
            >
            <span class="label-text text-base-content">Skip crop step</span>
          </label>
          <p class="text-xs leading-relaxed text-base-content/70">
            When enabled, you can bypass manual cropping and move straight to
            inference.
          </p>
        </div>
      </div>

      <template #actions>
        <button
          class="btn btn-primary"
          :disabled="isUploading || !uploads.length"
          @click="handleUpload"
        >
          <span
            v-if="isUploading"
            class="loading loading-spinner mr-2"
          />
          {{ isUploading ? "Uploading…" : "Next" }}
        </button>
      </template>
    </BaseCard>
    <BaseCard class="mt-6 mb-12 mx-4">
      <HowItWorksStrip />
    </BaseCard>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import BaseCard from "@/components/ui/BaseCard.vue";
import HowItWorksStrip from "../components/HowItWorksStrip.vue";
import { useBatchStore } from "@/stores/batch";

const router = useRouter();
const fileInput = ref(null);
const uploads = ref([]); // [{ file: File, url: string }]
const isUploading = ref(false);
const isDragging = ref(false);
const skipCrop = ref(false);
const batchStore = useBatchStore();

const triggerFileSelect = () => {
  fileInput.value?.click();
};

const onFileSelect = (e) => {
  handleFiles(e.target.files);
  // reset value so selecting the same file again triggers change
  e.target.value = "";
};

const onDragEnter = () => {
  isDragging.value = true;
};

const onDragLeave = () => {
  isDragging.value = false;
};

const onDrop = (e) => {
  isDragging.value = false;
  handleFiles(e.dataTransfer.files);
};

const handleFiles = (fileList) => {
  const remaining = 10 - uploads.value.length;
  const files = Array.from(fileList).slice(0, remaining);
  for (const file of files) {
    if (file.type.startsWith("image/")) {
      uploads.value.push({ file, url: URL.createObjectURL(file) });
    }
  }
  if (uploads.value.length >= 10 && fileList.length > remaining) {
    alert("You can upload up to 10 images.");
  }
};

const removeImage = (index) => {
  URL.revokeObjectURL(uploads.value[index].url);
  uploads.value.splice(index, 1);
};

const handleUpload = async () => {
  if (!uploads.value.length) {
    alert("Please choose a file first.");
    return;
  }
  isUploading.value = true;

  const formData = new FormData();
  for (const { file } of uploads.value) {
    formData.append("files", file); // match the parameter name in FastAPI
  }

  try {
    const res = await fetch("/api/batches", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) throw new Error(`Upload failed: ${res.status}`);

    const data = await res.json();
    const batchId = data?.batch_id ?? data?.id ?? data?.uuid;
    if (!batchId) throw new Error("Batch ID missing in response.");
    if (skipCrop.value) {
      queueAutoCropAndInfer(batchId);
      router.replace({
        name: "labelWizard",
        params: { id: batchId },
        query: { skipCrop: "true" },
      });
    } else {
      // Navigate to the first step, cropping
      router.replace({ name: "cropWizard", params: { id: batchId } });
    }
  } catch (err) {
    console.error("❌ Error uploading:", err);
    alert("Upload failed. Check console for details.");
  } finally {
    isUploading.value = false;
  }
};

const loadImageDimensions = (url) =>
  new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      resolve({ width: img.naturalWidth, height: img.naturalHeight });
    };
    img.onerror = (err) => reject(err);
    img.src = url;
  });

const queueAutoCropAndInfer = (batchId) => {
  // Fire-and-forget background processing; errors are logged but do not block navigation
  (async () => {
    try {
      const batch = await batchStore.getBatch(batchId);
      const specimens = batch?.specimens ?? [];

      await Promise.all(
        specimens.map(async (specimen) => {
          try {
            const info = specimen?.image_info ?? {};
            const sourceUrl = info.pre_crop_url || info.url;
            if (!specimen?.id || !sourceUrl) return;

            const { width, height } = await loadImageDimensions(sourceUrl);
            await batchStore.cropAndInfer(batchId, specimen.id, {
              x: 0,
              y: 0,
              width,
              height,
              rotate: 0,
            });
          } catch (specimenErr) {
            console.error(
              `Auto crop_and_infer failed for specimen ${specimen?.id}`,
              specimenErr
            );
          }
        })
      );
    } catch (err) {
      console.error("Auto crop_and_infer failed", err);
    }
  })();
};
</script>

<style scoped></style>
