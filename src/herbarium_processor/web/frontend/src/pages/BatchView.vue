<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Batch {{ id }}</h1>

    <div v-if="loading">Loading batch…</div>
    <div v-else-if="error" class="text-red-500">
      Failed to load batch: {{ error }}
    </div>
    <div v-else>
      <div v-if="images.length === 0" class="text-gray-500">
        No images in this batch.
      </div>
      <div v-else class="grid gap-4 grid-cols-2 md:grid-cols-3">
        <SpecimenCropView :image="images[0]"/>
        <div class="col-span-full text-gray-700 font-medium mb-2">
          {{ images.length }} image{{ images.length === 1 ? "" : "s" }} in this
          batch
        </div>
        <SpecimenCard
          v-for="img in images"
          :key="img.id"
          :image="img"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import SpecimenCard from "@/components/SpecimenCard.vue"
import SpecimenCropView from "@/components/SpecimenCropView.vue"
import { useBatchStore } from "@/stores/batch"   // our Pinia store

const props = defineProps({
  id: { type: String, required: true },
})

const images = ref([])
const loading = ref(true)
const error = ref(null)

const batchStore = useBatchStore()

onMounted(async () => {
  try {
    const batch = await batchStore.getBatch(props.id) // use store
    images.value = batch.images ?? []
  } catch (err) {
    error.value = err.message || "Unknown error"
  } finally {
    loading.value = false
  }
})
</script>
