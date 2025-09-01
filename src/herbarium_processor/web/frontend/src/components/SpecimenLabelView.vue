<template>
  <div
    class="mx-auto p-6 grid grid-cols-1 md:grid-cols-[1fr_auto] gap-6 h-screen"
  >
    <!-- Left card (stretches) -->
    <div class="card bg-base-100 shadow-xl overflow-hidden">
      <div class="card-body">
        <h2 class="card-title">{{ specimen.image_info.name }}</h2>
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
        <h2 class="card-title">Digitized fields</h2>
        <p class="text-xs leading-snug text-base-content/60">
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
          <div
            v-for="(val, key) in specimen.image_info?.llm_output ?? {}"
            :key="key"
            class="form-control mb-3"
          >
            <label class="label py-1">
              <span class="label-text text-xs">{{ key }}</span>
            </label>
            <textarea
              rows="1"
              class="textarea textarea-bordered textarea-sm w-full overflow-hidden max-h-60 [field-sizing:content] min-h-0 py-1"
              :value="String(val ?? '')">
            </textarea>
          </div>
        </div>
        <div class="card-actions justify-end sticky bottom-0 bg-base-100 py-2">
          <button class="btn btn-primary">Mark as reviewed</button>
          <button class="btn">Revert</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ImageExplorer from "@/components/ImageExplorer.vue";
const props = defineProps({
  specimen: { type: Object, required: true }, // {id, url, name, status?, fields?}
});
</script>

<style scoped>
/* ... */
</style>
