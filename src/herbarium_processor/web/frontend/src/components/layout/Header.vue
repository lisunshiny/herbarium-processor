<template>
  <header class="navbar bg-base-100 border-y border-base-300">
    <!-- Left: brand -->
    <div class="flex-1">
      <a href="/" class="pl-2 pr-2 text-xl cursor-pointer"
        >
        <img class="w-13 inline pr-2" :src="blob"></img>
        <span class="font-semibold">Parsely</span>
        <span class="font-light"> Studio</span> </a
      ><span
        class="badge badge-outline badge-xs badge-error translate-y-[-2px]"
      >
        Pre-alpha
      </span>
    </div>

    <!-- Right: nav items -->
    <div class="flex-none">
      <ul class="menu menu-horizontal px-1">
        <li>
          <RouterLink class="rounded-btn" to="/how-it-works">How it works</RouterLink>
        </li>
        <li>
          <RouterLink class="rounded-btn" to="/about">Our mission</RouterLink>
        </li>
      </ul>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router"
import blob from "@/assets/blob.svg";
</script>

<style scoped>
/* ... */
</style>
