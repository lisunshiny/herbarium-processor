<template>
  <div class="card bg-base-100 shadow">
    <div v-if="$slots.header" class="card-title px-6 pt-6">
      <slot name="header" />
    </div>

    <div class="card-body">
      <slot />
    </div>

    <div v-if="$slots.actions" class="card-actions justify-end px-6 pb-6">
      <slot name="actions" />
    </div>
  </div>
</template>
