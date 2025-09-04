<template>
  <BaseCard class="m-4">
    <template #header>Upload images</template>
    Upload up to 10 images at a time.
    <!-- File input -->
    <input
      ref="fileInput"
      type="file"
      multiple
      accept="image/*"
      class="file-input file-input-bordered w-full max-w-xs mb-4"
    />
    <template #actions>
      <button
        class="btn btn-primary"
        :disabled="isUploading"
        @click="handleUpload"
      >
        <span v-if="isUploading" class="loading loading-spinner mr-2"></span>
        {{ isUploading ? "Uploading…" : "Next" }}
      </button>
    </template>
  </BaseCard>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import BaseCard from "@/components/ui/BaseCard.vue";

const router = useRouter();
const fileInput = ref(null);
const isUploading = ref(false);

const handleUpload = async () => {
  if (!fileInput.value.files.length) {
    alert("Please choose a file first.");
    return;
  }
  isUploading.value = true;

  const formData = new FormData();
  for (const file of fileInput.value.files) {
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
    router.replace({ name: "cropWizard", params: { id: batchId } })
  } catch (err) {
    console.error("❌ Error uploading:", err);
    alert("Upload failed. Check console for details.");
  } finally {
    isUploading.value = false;
  }
};
</script>

<style scoped></style>
