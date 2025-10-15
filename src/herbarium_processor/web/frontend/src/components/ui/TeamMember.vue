<template>
  <div class="card bg-base-200/60 border border-base-300">
    <div class="card-body">
      <div class="flex items-center gap-5">
        <div class="avatar">
          <div
            class="w-24 sm:w-28 rounded-full ring ring-secondary/30 ring-offset-base-100 ring-offset-2"
          >
            <img
              :src="img"
              :alt="`Portrait of ${name}`"
            >
          </div>
        </div>
        <div class="min-w-0">
          <h3 class="text-xl font-semibold leading-tight">
            {{ name }}
            <span
              v-if="pronouns"
              class="ml-2 align-middle badge badge-neutral badge-sm"
            >
              {{ pronouns }}
            </span>
          </h3>
          <p class="text-sm text-base-content/70">
            {{ title }}
          </p>
        </div>
      </div>
      <p class="mt-4">
        <slot />
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: { type: String, required: true },
  pronouns: { type: String, default: '' },
  title: { type: String, required: true },
  img: { type: String, required: true },
})
</script>
