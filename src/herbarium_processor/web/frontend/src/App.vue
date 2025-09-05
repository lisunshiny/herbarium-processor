<template>
  <div class="min-h-screen bg-base-200 flex flex-col">
    <Header />
    <main class="flex-1">
      <router-view />
    </main>
    <Footer />

    <!-- Alert container -->
    <div class="toast">
      <div
        v-for="alert in alertStore.items"
        :key="alert.id"
        role="alert"
        :class="[
          'alert', // base class always
          {
            'alert-success': alert.type === 'success',
            'alert-info': alert.type === 'info',
            'alert-warning': alert.type === 'warning',
            'alert-error': alert.type === 'error',
          },
        ]"
      >
        <span>{{ alert.message }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import Header from "./components/layout/Header.vue";
import Footer from "./components/layout/Footer.vue";
import { useAlertStore } from "@/stores/alerts";

const alertStore = useAlertStore();
</script>

<style scoped></style>
