import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'

const routes = [
  { path: '/', component: Home },
  {
    path: "/batches/:id",
    name: "batch",
    component: () => import("@/pages/BatchView.vue"), // your crop/review UI
    props: true,
  },

  // Add more routes here as needed
]

export default createRouter({
  history: createWebHistory(), // history mode
  routes,
})
