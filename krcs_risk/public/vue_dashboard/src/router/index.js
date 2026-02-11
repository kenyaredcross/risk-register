import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/risks',
    name: 'RiskList',
    component: () => import('../views/RiskList.vue')
  },
  {
    path: '/risk/:id',
    name: 'RiskDetail',
    component: () => import('../views/RiskDetail.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
