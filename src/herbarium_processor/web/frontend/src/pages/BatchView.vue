<template>
  <WizardLayout :batchId="id">
    <!-- Top-of-content area -->
    <template #header>
      <div class="p-6">
        <h1 class="text-2xl font-bold">Batch {{ id }}</h1>
        <div v-if="loading" class="mt-2">Loading batch…</div>
        <div v-else-if="error" class="mt-2 text-red-500">Failed to load batch: {{ error }}</div>
      </div>
    </template>

    <!-- Main content: make it fill and scroll *inside* the middle pane if needed -->
    <div class="h-full px-6 pb-6">
      <div v-if="!loading && !error" class="h-full overflow-auto">
        <div v-if="specimens.length === 0" class="text-gray-500">
          No images in this batch.
        </div>
        <div v-else class="grid gap-4 grid-cols-2 md:grid-cols-3">
          <div class="col-span-full text-gray-700 font-medium mb-2">
            {{ specimens.length }} specimen{{ specimens.length === 1 ? "" : "s" }} in this batch
          </div>
          <SpecimenCard
            v-for="specimen in specimens"
            :key="specimen.image_info.id"
            :specimen="specimen"
          />
        </div>
      </div>
    </div>

    <!-- Bottom bar content -->
    <template #bottom-left>
      bottom left goes here
    </template>

    <template #bottom-right>
      bottom right goes here
    </template>
  </WizardLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useBatchStore } from "@/stores/batch"
import WizardLayout from "@/components/WizardLayout.vue"
import SpecimenCard from "@/components/SpecimenCard.vue"

const route = useRoute()
const router = useRouter()
const id = route.params.id

const specimens = ref([])
const loading = ref(true)
const error = ref(null)
const batchStore = useBatchStore()

onMounted(async () => {
  try {
    const batch = await batchStore.getBatch(id)
    specimens.value = batch.specimens ?? []
  } catch (err) {
    error.value = err?.message || "Unknown error"
  } finally {
    loading.value = false
  }
})

function goToCrop()   { router.push({ name: "wizard", params: { id }, query: { step: 0 } }) }
function goToReview() { router.push({ name: "wizard", params: { id }, query: { step: 1 } }) }
</script>
