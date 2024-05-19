import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/sourcelist',
      name: 'sourcelist',
      component: () => import('../views/Sourcelist.vue')
    },
    {
      path: '/add',
      name: 'add',
      component: () => import('../views/AddSourceView.vue')
    },
    {
      path: '/viewstories/:id&name=:source_name',
      name: 'stories',
      component: () => import('../views/Stories.vue')
    }
    ,
    {
      path: '/',
      name: 'recommended',
      component: () => import('../views/Recommended.vue')
    }
  ]
})

export default router
