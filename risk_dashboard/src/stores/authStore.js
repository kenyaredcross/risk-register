import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const KRCS_ROLES = new Set([
  'System Manager',
  'KRCS HOR',
  'KRCS DSG',
  'KRCS HOD',
  'KRCS Project Manager',
  'KRCS RPC',
  'KRCS Finance Officer',
  'KRCS Procurement Manager',
  'KRCS Logistics Manager',
  'KRCS HR Manager',
  'KRCS Audit',
])

export const useAuthStore = defineStore('auth', () => {
  // State — resolved via session API on first navigation
  const user = ref(null)
  const fullName = ref('')
  const roles = ref([])

  const isLoggedIn = computed(() => !!user.value && user.value !== 'Guest')
  const isSystemManager = computed(() => roles.value.includes('System Manager'))
  const isHOD = computed(() => roles.value.includes('KRCS HOD'))
  const isHOR = computed(() => roles.value.includes('KRCS HOR'))
  const isAudit = computed(() => roles.value.includes('KRCS Audit'))
  const isPM = computed(() => roles.value.includes('KRCS Project Manager'))
  // HOD and PM can access the Users admin page to manage users in their department
  const canManageUsers = computed(() => isSystemManager.value || isHOD.value || isPM.value)
  // True if user has at least one KRCS role (required for all dashboard access)
  const hasKrcsRole = computed(() => roles.value.some(r => KRCS_ROLES.has(r)))

  /**
   * Login via Frappe's login endpoint.
   * Returns { success: true } or { success: false, message: '...' }
   */
  const login = async (usr, pwd) => {
    try {
      const response = await axios.post(
        '/api/method/login',
        new URLSearchParams({ usr, pwd }),
        {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          withCredentials: true,
        }
      )
      const data = response.data
      // Frappe returns { message: 'Logged In', home_page: '...' }
      if (data.message === 'Logged In' || data.message === 'No App') {
        // Fetch current user info
        await fetchCurrentUser()
        return { success: true }
      }
      return { success: false, message: data.message || 'Login failed.' }
    } catch (err) {
      const msg =
        err.response?.data?.message ||
        err.response?.data?.exc_type ||
        'Incorrect email or password.'
      return { success: false, message: msg }
    }
  }

  /**
   * Fetch the currently logged-in user from Frappe.
   * Uses our own get_current_user API so that roles are always readable
   * regardless of the user's permission level (Frappe's resource API blocks
   * reading the roles child table for non-System Manager users).
   */
  const fetchCurrentUser = async () => {
    try {
      // First confirm we have a logged-in session
      const res = await axios.get('/api/method/frappe.auth.get_logged_user')
      user.value = res.data.message || null

      if (user.value && user.value !== 'Guest') {
        // Our endpoint returns all_roles (full role list), full_name, etc.
        const meRes = await axios.get(
          '/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_current_user'
        )
        const me = meRes.data.message || {}
        fullName.value = me.full_name || user.value
        // all_roles contains every role the user has (including System Manager)
        roles.value = me.all_roles || []
      }
    } catch {
      user.value = null
      fullName.value = ''
      roles.value = []
    }
  }

  /**
   * Logout via Frappe's logout endpoint.
   */
  const logout = async () => {
    try {
      // Get CSRF token from cookie
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrf_token='))
        ?.split('=')[1]

      await axios.post('/api/method/logout', {}, {
        withCredentials: true,
        headers: {
          'X-Frappe-CSRF-Token': csrfToken || 'fetch'
        }
      })
    } catch (err) {
      console.error('Logout error:', err)
      // ignore errors — clear state regardless
    }

    // Clear local state
    user.value = null
    fullName.value = ''
    roles.value = []

    // Redirect to login page (Frappe's standard login)
    window.location.href = '/login'
  }

  /**
   * Check session on app boot (called once from main.js).
   */
  const checkSession = async () => {
    await fetchCurrentUser()
  }

  return { user, fullName, roles, isLoggedIn, isSystemManager, isHOD, isHOR, isAudit, isPM, canManageUsers, hasKrcsRole, login, logout, checkSession }
})
