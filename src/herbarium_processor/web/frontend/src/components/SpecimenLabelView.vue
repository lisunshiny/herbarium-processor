<template>
  <div
    class="mx-auto p-6 grid grid-cols-1 md:grid-cols-[1fr_auto] gap-6 h-screen"
  >
    <!-- Left card (stretches) -->
    <div class="card bg-base-100 shadow-xl overflow-hidden">
      <div class="card-body">
        <h2 class="card-title">{{ specimen.image_info.name }}
        </h2>
        <ImageExplorer
          :specimen="specimen"
          :image_url="specimen.image_info.ocr_bounding_url"
          class="h-[70vh]"
        />
      </div>
    </div>

    <!-- Right card (fixed w-64, scrollable) -->
    <div class="card bg-base-100 shadow-xl w-64 overflow-y-auto">
      <div class="card-body">
        <h2 class="card-title">Digitized fields
                    <div v-if="!specimen.image_info.user_edited_llm_output" class="badge badge-xs badge-outline badge-warning">Needs review</div>
          <div v-else class="badge badge-xs badge-outline badge-success">Reviewed</div>

        </h2>
        <p v-if="!specimen.image_info.user_edited_llm_output" class="text-xs leading-snug text-base-content/60">
          These fields were autocompleted by an AI model and may contain errors.
          Please review and correct before finalizing.
        </p>
        <div
          v-if="!specimen.image_info.llm_output"
          class="text-sm text-base-content/60"
        >
          No extracted fields yet.
        </div>
        <div v-else>
          <div v-for="(val, key) in form" :key="key" class="form-control mb-3">
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

        <div class="card-actions justify-end sticky bottom-0 bg-base-100 py-2">
          <button class="btn btn-primary" @click="saveLabel">
            <span v-if="!specimen.image_info.user_edited_llm_output">Mark as reviewed</span>
            <span v-else>Update</span>
          </button>
          <button class="btn" @click="revert">Revert</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { watch, reactive } from "vue"
import { useBatchStore } from "@/stores/batch"
import ImageExplorer from "@/components/ImageExplorer.vue"

const props = defineProps({
  batchId: { type: String, required: true },
  specimen: { type: Object, required: true }, // {id, url, name, status?, fields?}
});

const batchStore = useBatchStore();

const form = reactive({
  ...(props.specimen?.image_info?.llm_output || {})
})

// Helper to reset form from a source object (keeps reactivity)
function setFormFrom(obj) {
  // remove keys that no longer exist
  for (const k of Object.keys(form)) {
    if (!(obj && Object.prototype.hasOwnProperty.call(obj, k))) {
      delete form[k]
    }
  }
  // copy over current keys
  if (obj) {
    for (const [k, v] of Object.entries(obj)) {
      form[k] = v
    }
  }
}

function revert() {
  setFormFrom(props.specimen?.image_info?.llm_output || {})
}

async function saveLabel() {
    // send a plain object (avoid serializing proxies)
  const payload = JSON.parse(JSON.stringify(form))

  const updated_specimen = await batchStore.postUserUpdatedLlmLabels(
    props.batchId,
    props.specimen.image_info.id,
    payload
  );
  console.log("saving!", payload)
}
watch(
  () => props.specimen?.image_info?.llm_output,
  (newVal) => setFormFrom(newVal || {}),
  { immediate: true, deep: true }
)

</script>

<style scoped>
/* ... */
</style>
