import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/add',
      name: 'add',
      component: () => import('../views/AddSourceView.vue')
    },
    {
      path: '/viewstories/:id',
      name: 'stories',
      component: () => import('../views/Stories.vue')
    }
  ]
})

export default router
