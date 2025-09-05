<template>
  <div class="m-4 space-y-4">
    <div
      class="w-full rounded-lg bg-gradient-to-r from-info to-blue-500 text-white py-3 px-6 text-center shadow-md"
    >
      <span class="font-bold"
        >✨ Parsely Studio is just getting started! ✨</span
      ><br/>
      <span class="ml-2"
        >Help shape the journey — reach us at
        <a
          href="mailto:danielleward@berkeley.edu"
          class="underline font-semibold"
          >danielleward@berkeley.edu</a
        >.
      </span>
    </div>

    <BaseCard>
      <template #header>Upload photos of specimens</template>
      <!-- Drop zone -->
      <div
        :class="[
          'border-2 border-dashed rounded p-12 text-center cursor-pointer',
          isDragging ? 'border-primary bg-base-200' : 'border-base-300'
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
      />

      <!-- Thumbnails -->
      <div v-if="uploads.length" class="flex flex-wrap gap-4 mt-4">
        <div
          v-for="(upload, index) in uploads"
          :key="index"
          class="relative w-24 h-24"
        >
          <img
            :src="upload.url"
            alt="preview"
            class="object-cover w-full h-full rounded"
          />
          <button
            type="button"
            class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center"
            @click="removeImage(index)"
          >
            &times;
          </button>
        </div>
      </div>

      <template #actions>
        <button
          class="btn btn-primary"
          :disabled="isUploading || !uploads.length"
          @click="handleUpload"
        >
          <span v-if="isUploading" class="loading loading-spinner mr-2"></span>
          {{ isUploading ? "Uploading…" : "Next" }}
        </button>
      </template>
    </BaseCard>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import BaseCard from "@/components/ui/BaseCard.vue";

const router = useRouter();
const fileInput = ref(null);
const uploads = ref([]); // [{ file: File, url: string }]
const isUploading = ref(false);
const isDragging = ref(false);

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

    // Navigate to the first step, cropping
    router.replace({ name: "cropWizard", params: { id: batchId } });
  } catch (err) {
    console.error("❌ Error uploading:", err);
    alert("Upload failed. Check console for details.");
  } finally {
    isUploading.value = false;
  }
};
</script>

<style scoped></style>
