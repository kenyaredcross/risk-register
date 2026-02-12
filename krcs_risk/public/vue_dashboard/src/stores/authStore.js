import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  // State — resolved via session API on first navigation
  const user = ref(null)
  const fullName = ref('')
  const roles = ref([])

  const isLoggedIn = computed(() => !!user.value && user.value !== 'Guest')
  const isSystemManager = computed(() => roles.value.includes('System Manager'))

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
   */
  const fetchCurrentUser = async () => {
    try {
      const res = await axios.get('/api/method/frappe.auth.get_logged_user')
      user.value = res.data.message || null
      // Also grab full name and roles
      if (user.value && user.value !== 'Guest') {
        const userRes = await axios.get(`/api/resource/User/${user.value}`, {
          params: { fields: JSON.stringify(['full_name', 'roles']) }
        })
        fullName.value = userRes.data.data?.full_name || user.value
        // Extract role names from roles child table
        const userRoles = userRes.data.data?.roles || []
        roles.value = userRoles.map(r => r.role)
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
      await axios.post('/api/method/logout', {}, { withCredentials: true })
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

  return { user, fullName, roles, isLoggedIn, isSystemManager, login, logout, checkSession }
})
