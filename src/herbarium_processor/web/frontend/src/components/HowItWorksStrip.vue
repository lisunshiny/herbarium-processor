<!-- src/components/HowItWorksStrip.vue -->

<template>
  <div
    class="grid grid-cols-1 sm:grid-cols-4 gap-6"
  >
    <div class="text-center">
      <div
        class="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 ring-1 ring-slate-200 mx-auto"
      >
        <Upload class="h-5 w-5 text-slate-700" />
      </div>
      <h3 class="font-medium text-slate-900">Upload your specimen</h3>
      <p class="mt-1 text-sm text-slate-600">
        Snap a quick photo on your phone or drop in any image with the label
        showing. Don’t worry about the angle — we’ll fix the rotation and
        cropping together.
      </p>
    </div>
    <div class="text-center">
      <div
        class="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 ring-1 ring-slate-200 mx-auto"
      >
        <Crop class="h-5 w-5 text-slate-700" />
      </div>
      <h3 class="font-medium text-slate-900">Adjust the view</h3>
      <p class="mt-1 text-sm text-slate-600">
        If needed, rotate the image or trim the edges so that it's just the
        label.
      </p>
    </div>
    <div class="text-center">
      <div
        class="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 ring-1 ring-slate-200 mx-auto"
      >
        <ScanText class="h-5 w-5 text-slate-700" />
      </div>
      <h3 class="font-medium text-slate-900">
        Let the AI do the heavy lifting
      </h3>
      <p class="mt-1 text-sm text-slate-600">
        We’ll pull out the details for you — collector, date, location, catalog
        number, taxon, and more — so you don’t have to type them in.
      </p>
    </div>
    <div class="text-center">
      <div
        class="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 ring-1 ring-slate-200 mx-auto"
      >
        <FileDown class="h-5 w-5 text-slate-700" />
      </div>
      <h3 class="font-medium text-slate-900">Review & export</h3>
      <p class="mt-1 text-sm text-slate-600">
        Give everything a quick once-over, make edits right on the page, and
        then export your data as CSV to use however you like.
      </p>
    </div>
  </div>
</template>

<script setup>
import { Upload, Crop, ScanText, FileDown } from "lucide-vue-next";

</script>

<style scoped></style>
