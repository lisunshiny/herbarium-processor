import { defineStore } from 'pinia';

let nextId = 1;

export const useAlertStore = defineStore('alerts', {
  state: () => ({
    /** @type {{id:number, message:string, type:string}[]} */
    items: [],
  }),
  actions: {
    /**
     * Add a new alert to the list.
     * @param {string} message
     * @param {string} [type='success']
     * @param {number} [timeout=5000]
     * @returns {number} id of the alert
     */
    addAlert(message, type = 'success', timeout = 5000) {
      const id = nextId++;
      this.items.push({ id, message, type });
      if (timeout) {
        setTimeout(() => {
          this.removeAlert(id);
        }, timeout);
      }
      return id;
    },
    /** Remove an alert by id */
    removeAlert(id) {
      this.items = this.items.filter((a) => a.id !== id);
    },
  },
});

