<!-- src/components/HowItWorksStrip.vue -->

<template>
  <div class="grid grid-cols-1 sm:grid-cols-4 gap-6">
    <div class="text-center">
      <div
        class="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 ring-1 ring-slate-200 mx-auto">
        <Upload class="h-5 w-5 text-slate-700" />
      </div>
      <h3 class="font-medium text-slate-900">Upload your specimen</h3>
    </div>
    <div class="text-center">
      <div
        class="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 ring-1 ring-slate-200 mx-auto">
        <Crop class="h-5 w-5 text-slate-700" />
      </div>
      <h3 class="font-medium text-slate-900">Adjust the view</h3>
    </div>
    <div class="text-center">
      <div
        class="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 ring-1 ring-slate-200 mx-auto">
        <ScanText class="h-5 w-5 text-slate-700" />
      </div>
      <h3 class="font-medium text-slate-900">
        Let AI parse the text
      </h3>
    </div>
    <div class="text-center">
      <div
        class="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 ring-1 ring-slate-200 mx-auto">
        <FileDown class="h-5 w-5 text-slate-700" />
      </div>
      <h3 class="font-medium text-slate-900">Review & export</h3>
    </div>
  </div>
</template>

<script setup>
import { Upload, Crop, ScanText, FileDown } from "lucide-vue-next";
</script>

<style scoped></style>
