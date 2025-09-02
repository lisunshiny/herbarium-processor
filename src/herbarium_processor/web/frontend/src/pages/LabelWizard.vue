<template>
  <StatusBar :id="id" />
  <div class="">
    <!-- <h1 class="text-2xl font-bold mb-4">Batch {{ id }}</h1> -->

    <div v-if="loading">Loading batch…</div>
    <div v-else-if="error" class="text-red-500">
      Failed to load batch: {{ error }}
    </div>
    <div v-else>
      <div v-if="specimens.length === 0" class="text-gray-500">
        No images in this batch.
      </div>
    <div v-else>
      <BaseCard class="max-w-5xl mx-auto">
        <SpecimenLabelView
          v-for="specimen in specimens"
          :key="specimen.image_info.id"
          :specimen="specimen"
          :batchId="id"
        />
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import SpecimenLabelView from "@/components/SpecimenLabelView.vue"
import StatusBar from "@/components/StatusBar.vue"
import BaseCard from "@/components/ui/BaseCard.vue"
import { useBatchStore } from "@/stores/batch"   // our Pinia store

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
    }
  } catch (err) {
    error.value = err.message || "Unknown error"
  } finally {
    loading.value = false
  }
})
</script>
