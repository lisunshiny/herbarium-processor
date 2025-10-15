<template>
  <div class="min-h-screen bg-base-200 flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <router-view />
    </main>
    <AppFooter />

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
import AppHeader from "./components/layout/AppHeader.vue";
import AppFooter from "./components/layout/AppFooter.vue";
import { useAlertStore } from "@/stores/alerts";

const alertStore = useAlertStore();
</script>

<style scoped></style>
