// src/stores/batch.js
import { defineStore } from "pinia";

export const useBatchStore = defineStore("batches", {
  state: () => ({
    // Acts as an in-memory cache: { [id]: Batch }
    batches: {},
  }),
  actions: {
    getItemsInEachState(id) {
      const batch = this.batches[id];
      if (!batch || !batch.images) return { cropping: 0, digitizing: 0, ready: 0 };

      let cropping = 0, digitizing = 0, ready = 0;
      for (const img of batch.images) {
        if (!img.post_crop_url || img.post_crop_url === "") {
          cropping++;
        } else if (!img.llm_output || img.llm_output === "") {
          digitizing++;
        } else {
          ready++;
        }
      }
      return { cropping, digitizing, ready };
    },
    getBatchState(id) {
      if(this.getItemsInEachState(id).cropping > 0) return "cropping";
      return "digitizing";
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
