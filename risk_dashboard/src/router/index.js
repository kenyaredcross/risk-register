import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { public: true }
  },
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
    path: '/risk/create',
    name: 'RiskCreate',
    component: () => import('../views/RiskCreate.vue')
  },
  {
    path: '/risk/:id',
    name: 'RiskDetail',
    component: () => import('../views/RiskDetail.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue')
  },
  {
    path: '/admin/departments',
    name: 'AdminDepartments',
    component: () => import('../views/admin/Departments.vue'),
    meta: { requiresSystemManager: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/admin/Users.vue'),
    meta: { requiresSystemManager: true }
  },
  {
    path: '/admin/roles',
    name: 'AdminRoles',
    component: () => import('../views/admin/Roles.vue'),
    meta: { requiresSystemManager: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// Navigation guard — redirect unauthenticated users to /login
router.beforeEach(async (to) => {
  if (to.meta.public) return true

  const authStore = useAuthStore()

  // First navigation — check session against Frappe
  if (authStore.user === null) {
    await authStore.checkSession()
  }

  if (!authStore.isLoggedIn) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  // Check System Manager requirement for admin routes
  if (to.meta.requiresSystemManager && !authStore.isSystemManager) {
    return { name: 'Dashboard' }
  }

  return true
})

export default router
