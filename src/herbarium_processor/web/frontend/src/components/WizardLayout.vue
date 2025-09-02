<template>
  <!-- Full-screen, no page scroll -->
  <div class="fixed inset-0 flex flex-col bg-base-100">
    <!-- Top bar stays the same across steps -->
    <StatusBar :id="batchId" />

    <!-- Middle content fills the space between bars -->
    <div class="flex-1 overflow-hidden">
      <!-- Force children to be able to 100% height -->
      <div class="h-full">
        <!-- Optional top-of-content area (e.g., title, alerts) -->
        <slot name="header" />

        <!-- Main step content goes here -->
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

const props = defineProps({
  batchId: { type: String, required: true },
})
</script>
