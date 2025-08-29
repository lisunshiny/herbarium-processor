import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'

const routes = [
  { path: '/', component: Home },
  // Add more routes here as needed
]

export default createRouter({
  history: createWebHistory(), // history mode
  routes,
})
