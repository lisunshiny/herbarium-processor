<template>
  <footer class="w-full bg-base-200 text-base-content">
    <div class="mx-auto max-w-6xl px-4 py-4">
      <div class="flex flex-col items-center gap-1 text-sm md:flex-row md:justify-between md:gap-4">
        <p class="font-medium">Parsely is made with ❤️ in Oakland, CA</p>

        <p class="font-medium">
          Let’s chat:
          <a
            :href="mailto"
            class="link link-hover"
            :aria-label="ariaLabel"
          >
            {{ email }}
          </a>
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from "vue"

// Obfuscate in source; show visibly
const u = "hello"
const d = "parselyapp.com"

const email = computed(() => `${u}@${d}`)
const mailto = computed(() => `mailto:${email.value}`)
const ariaLabel = computed(() => `Email ${email.value}`)
</script>
