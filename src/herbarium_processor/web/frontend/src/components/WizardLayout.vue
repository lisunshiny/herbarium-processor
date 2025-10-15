<template>
  <!-- 3 rows: header | content | footer -->
  <div class="fixed inset-0 grid grid-rows-[auto_1fr_auto] bg-base-100">
    <!-- Top bar -->
    <StatusBar :id="batchId" />

    <!-- Middle slot fills exactly between bars -->
    <div class="overflow-hidden">
      <div class="h-full">
        <slot />
      </div>
    </div>

    <!-- Bottom bar stays the same across steps; provide two slots -->
    <BottomBar :id="batchId">
      <template #left>
        <slot name="bottom-left" />
      </template>
      <template #right>
        <slot name="bottom-right" />
      </template>
    </BottomBar>
  </div>
</template>

<script setup>
import StatusBar from "@/components/StatusBar.vue"
import BottomBar from "@/components/BottomBar.vue"

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  batchId: { type: String, required: true },
})
</script>
