<template>
  <div class="min-h-screen w-full bg-white text-slate-900">
    <main class="mx-auto">
      <!-- Hero header -->
      <div class="max-w-4xl mx-auto px-6 pt-12 pb-6">
        <h1 class="text-4xl font-bold tracking-tight mb-4">
          From photo to structured data—<span class="text-slate-600">in less than a minute</span>.
        </h1>

        <p class="text-lg text-slate-600">
          Parsely Studio transforms herbarium specimen photos into clean,
          reviewable fields in four easy steps — fast, accurate, and effortless.
        </p>
      </div>
      <div class="">
        <div class="max-w-4xl mx-auto px-6 pb-12">
          <h2 class="text-xl mb-4 font-medium">
            See it in action
          </h2>
          <SampleLabelSelector />
        </div>
      </div>

      <div class="bg-base-200 py-12">
        <HowItWorksStrip class="max-w-4xl mx-auto" />
      </div>
      <section class="mx-auto max-w-4xl px-6 py-12">
        <div class="">
          <div class="px-6 sm:px-10 py-10 text-center">
            <h3 class="text-2xl font-semibold tracking-tight">
              Ready to get started?
            </h3>
            <p class="mt-2 text-base text-base-content/70">
              Upload a label photo and see structured fields in seconds.
            </p>

            <div class="mt-6 flex items-center justify-center gap-3">
              <a
                href="/"
                class="btn btn-neutral btn-lg rounded-2xl px-6"
                aria-label="Try Parsely Studio now"
              >
                Try it out
                <span aria-hidden>→</span>
              </a>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>
<script setup>
import SampleLabelSelector from "../components/SampleLabelSelector.vue";
import HowItWorksStrip from "../components/HowItWorksStrip.vue";
</script>
``
