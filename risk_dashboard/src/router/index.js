import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const PREF_KEY = 'krcs_primary_dashboard'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { public: true }
  },
  {
    // "/" redirects to the user's preferred primary dashboard
    path: '/',
    name: 'Home',
    redirect: () => {
      const pref = localStorage.getItem(PREF_KEY) || 'risk'
      return pref === 'matrix' ? '/matrix' : '/dashboard'
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/matrix',
    name: 'CategoryMatrix',
    component: () => import('../views/RiskCategoryMatrix.vue')
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
    meta: { requiresDepartmentManager: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/admin/Users.vue'),
    meta: { requiresUserManager: true }
  },
  {
    path: '/admin/roles',
    name: 'AdminRoles',
    component: () => import('../views/admin/Roles.vue'),
    meta: { requiresSystemManager: true }
  },
  {
    path: '/coi-dashboard',
    name: 'COIDashboard',
    component: () => import('../views/COIDashboard.vue')
  },
  {
    path: '/coi-declaration/create',
    name: 'COIDeclarationCreate',
    component: () => import('../views/COIDeclaration.vue')
  },
  {
    path: '/coi-declarations',
    name: 'COIDeclarations',
    component: () => import('../views/COIDeclarationList.vue')
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

  // User is logged in but has no KRCS role — send back to Frappe login
  if (!authStore.hasKrcsRole) {
    window.location.href = '/login'
    return false
  }

  // Check System Manager requirement for admin routes (roles reference)
  if (to.meta.requiresSystemManager && !authStore.isSystemManager) {
    return { name: 'Dashboard' }
  }

  // Check department manager requirement (System Manager or KRCS HOD can manage units)
  if (to.meta.requiresDepartmentManager && !authStore.isSystemManager && !authStore.isHOD) {
    return { name: 'Dashboard' }
  }

  // Check user-manager requirement (System Manager, KRCS HOD, or KRCS PM)
  if (to.meta.requiresUserManager && !authStore.canManageUsers) {
    return { name: 'Dashboard' }
  }

  return true
})

export default router
