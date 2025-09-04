<template>
  <div class="min-h-screen bg-base-200 flex flex-col">
    <Header />
    <main class="flex-1">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from "./components/layout/Header.vue";
import Footer from "./components/layout/Footer.vue";
</script>

<style scoped></style>
