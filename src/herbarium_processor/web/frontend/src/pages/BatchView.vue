<template>
  <StatusBar :id="id" class="mb-4" />
  <div class="">
    <h1 class="text-2xl font-bold mb-4">Batch {{ id }}</h1>

    <div v-if="loading">Loading batch…</div>
    <div v-else-if="error" class="text-red-500">
      Failed to load batch: {{ error }}
    </div>
    <div v-else>
      <div v-if="specimens.length === 0" class="text-gray-500">
        No images in this batch.
      </div>
      <div v-else class="grid gap-4 grid-cols-2 md:grid-cols-3">
        <div class="col-span-full text-gray-700 font-medium mb-2">
          {{ specimens.length }} specimens{{ specimens.length === 1 ? "" : "s" }} in this
          batch
        </div>
        <SpecimenCard
          v-for="specimen in specimens"
          :key="specimen.image_info.id"
          :specimen="specimen"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import SpecimenCard from "@/components/SpecimenCard.vue"
import { useBatchStore } from "@/stores/batch"   // our Pinia store
import StatusBar from "@/components/StatusBar.vue";

const props = defineProps({
  id: { type: String, required: true },
})

const router = useRouter()
const specimens = ref([])
const loading = ref(true)
const error = ref(null)

const batchStore = useBatchStore()

onMounted(async () => {
  try {
    const batch = await batchStore.getBatch(props.id) // use store
    specimens.value = batch.specimens ?? []

    // Auto-navigate to CropWizard if the stage is "cropping"
    const stage = batchStore.getBatchState(props.id)
    if (stage === "cropping") {
      router.replace({ name: "cropWizard", params: { id: props.id } })
      return
    } else if (stage === "labeling") {
      router.replace({ name: "labelWizard", params: { id: props.id } })
      return
    }
  } catch (err) {
    error.value = err.message || "Unknown error"
  } finally {
    loading.value = false
  }
})
</script>
