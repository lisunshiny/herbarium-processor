// src/stores/batch.js
import { defineStore } from "pinia";

export const useBatchStore = defineStore("batches", {
  state: () => ({
    // Acts as an in-memory cache: { [id]: Batch }
    batches: {},
  }),
  actions: {
    getBatchState(id) {
      return "crop";
    },
    /**
     * Returns the batch for `id`.
     * - If already cached, returns it immediately.
     * - Otherwise fetches from `/api/batches/:id`, stores it, then returns.
     */
    async getBatch(id) {
      if (this.batches[id]) {
        // cache hit
        return this.batches[id];
      }

      // cache miss
      const res = await fetch(`/api/batches/${id}`);
      if (!res.ok) throw new Error(`Failed to fetch ${id}`);

      const data = await res.json();
      this.batches[id] = data;
      return data;
    },
  },
});
