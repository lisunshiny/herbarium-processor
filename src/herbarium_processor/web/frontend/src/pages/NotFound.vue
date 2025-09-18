<template>
  <section class="hero min-h-[60vh] bg-base-200">
    <div class="hero-content text-center">
      <div class="max-w-md">
        <h1 class="text-5xl font-bold mb-4">Page not found</h1>
        <p class="mb-6 text-lg">
          The page you are looking for doesn&apos;t exist or has been moved.
        </p>
        <RouterLink class="btn btn-primary" to="/">
          Go back home
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>
