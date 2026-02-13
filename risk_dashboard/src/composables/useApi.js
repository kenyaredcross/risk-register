import { ref } from 'vue'
import axios from 'axios'

// Axios is configured globally in main.js

export function useApi() {
  const loading = ref(false)
  const error = ref(null)

  /**
   * Fetch all risks from Frappe backend
   */
  const fetchRisks = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await axios.get('/api/resource/Program Risk Register', {
        params: {
          fields: JSON.stringify([
            'name',
            'project',
            'risk_category',
            'risk_description',
            'likelihood',
            'impact',
            'overall_rating',
            'risk_level',
            'risk_owner',
            'department',
            'region',
            'status',
            'review_frequency',
            'next_review_due',
            'review_status',
            'timeline',
            'status',
            'approved_by',
            'approval_date',
            'rejection_reason',
            'creation',
            'modified'
          ]),
          limit_page_length: 0 // Get all records
        }
      })

      return response.data.data || []
    } catch (err) {
      error.value = err.message || 'Failed to fetch risks'
      console.error('API Error:', err)
      return []
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch a single risk by name
   */
  const fetchRisk = async (name) => {
    loading.value = true
    error.value = null

    try {
      const response = await axios.get(`/api/resource/Program Risk Register/${name}`)
      return response.data.data || null
    } catch (err) {
      error.value = err.message || 'Failed to fetch risk'
      console.error('API Error:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Get risk statistics
   */
  const getRiskStats = (risks) => {
    const stats = {
      total: risks.length,
      critical: 0,
      high: 0,
      medium: 0,
      low: 0,
      overdue: 0,
      dueSoon: 0,
      byDepartment: {},
      byStatus: {},
      averageRating: 0
    }

    let totalRating = 0

    risks.forEach(risk => {
      // Count by risk level
      const level = (risk.risk_level || '').toLowerCase()
      if (level === 'critical') stats.critical++
      else if (level === 'high') stats.high++
      else if (level === 'medium') stats.medium++
      else if (level === 'low') stats.low++

      // Count by review status
      if (risk.review_status === 'Overdue') stats.overdue++
      else if (risk.review_status === 'Due Soon') stats.dueSoon++

      // Count by department
      const dept = risk.department || 'Unassigned'
      stats.byDepartment[dept] = (stats.byDepartment[dept] || 0) + 1

      // Count by status
      const status = risk.status || 'Unknown'
      stats.byStatus[status] = (stats.byStatus[status] || 0) + 1

      // Sum ratings
      totalRating += risk.overall_rating || 0
    })

    stats.averageRating = stats.total > 0 ? (totalRating / stats.total).toFixed(1) : 0

    return stats
  }

  /**
   * Get risk matrix data (5x5 grid)
   */
  const getRiskMatrix = (risks) => {
    // Initialize 5x5 matrix
    const matrix = Array(5).fill(null).map(() => Array(5).fill(0))
    const risksByCell = Array(5).fill(null).map(() => Array(5).fill(null).map(() => []))

    risks.forEach(risk => {
      const likelihood = (risk.likelihood || 1) - 1 // Convert 1-5 to 0-4
      const impact = (risk.impact || 1) - 1

      if (likelihood >= 0 && likelihood < 5 && impact >= 0 && impact < 5) {
        matrix[4 - impact][likelihood]++ // Flip impact for display (high at top)
        risksByCell[4 - impact][likelihood].push(risk)
      }
    })

    return { matrix, risksByCell }
  }

  /**
   * Add a new risk review
   */
  const addRiskReview = async (riskName, reviewData) => {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.add_risk_review', {
        risk_name: riskName,
        review_date: reviewData.review_date,
        reviewed_by: reviewData.reviewed_by,
        summary: reviewData.summary,
        actions: reviewData.actions,
        next_review_date: reviewData.next_review_date
      })

      return response.data.message || {}
    } catch (err) {
      error.value = err.message || 'Failed to add review'
      console.error('API Error:', err)
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * Update an existing risk review
   */
  const updateRiskReview = async (riskName, reviewIdx, reviewData) => {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.update_risk_review', {
        risk_name: riskName,
        review_idx: reviewIdx,
        review_date: reviewData.review_date,
        reviewed_by: reviewData.reviewed_by,
        summary: reviewData.summary,
        actions: reviewData.actions,
        next_review_date: reviewData.next_review_date
      })

      return response.data.message || {}
    } catch (err) {
      error.value = err.message || 'Failed to update review'
      console.error('API Error:', err)
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * Delete a risk review
   */
  const deleteRiskReview = async (riskName, reviewIdx) => {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.delete_risk_review', {
        risk_name: riskName,
        review_idx: reviewIdx
      })

      return response.data.message || {}
    } catch (err) {
      error.value = err.message || 'Failed to delete review'
      console.error('API Error:', err)
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * Get current user's approval roles (generic, not risk-specific)
   */
  const getUserRoles = async () => {
    try {
      const res = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_user_roles')
      return res.data.message || { is_any_approver: false, is_global_approver: false, roles: [] }
    } catch {
      return { is_any_approver: false, is_global_approver: false, roles: [] }
    }
  }

  /**
   * Check if current user can approve/reject a specific risk (scoped check)
   */
  const canApproveRisk = async (riskName) => {
    try {
      const res = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.can_approve_risk', {
        params: { risk_name: riskName }
      })
      return res.data.message || { can_approve: false, status: '' }
    } catch {
      return { can_approve: false, status: '' }
    }
  }

  /**
   * Submit a risk for approval (Draft/Rejected → Pending Approval)
   */
  const submitForApproval = async (riskName) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.submit_for_approval', {
        risk_name: riskName
      })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to submit for approval.' }
    }
  }

  /**
   * Request closure of a risk (Open → Pending Close Approval)
   */
  const requestClose = async (riskName) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.request_close', {
        risk_name: riskName
      })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to request closure.' }
    }
  }

  /**
   * Approve a pending risk (Approver only)
   */
  const approveRisk = async (riskName) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.approve_risk', {
        risk_name: riskName
      })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to approve risk.' }
    }
  }

  /**
   * Reject a pending risk (Approver only)
   */
  const rejectRisk = async (riskName, reason) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.reject_risk', {
        risk_name: riskName,
        reason: reason || ''
      })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to reject risk.' }
    }
  }

  // ---------------------------------------------------------------------------
  // Admin APIs (System Manager only)
  // ---------------------------------------------------------------------------

  /**
   * Get all departments with their units
   */
  const getDepartments = async () => {
    try {
      const res = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_departments')
      return res.data.message || []
    } catch {
      return []
    }
  }

  /**
   * Create a new department
   */
  const createDepartment = async (departmentName) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.create_department', {
        department_name: departmentName
      })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to create department.' }
    }
  }

  /**
   * Delete a department
   */
  const deleteDepartment = async (name) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.delete_department', { name })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to delete department.' }
    }
  }

  /**
   * Create a new unit under a department
   */
  const createUnit = async (unitName, department) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.create_unit', {
        unit_name: unitName,
        department
      })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to create unit.' }
    }
  }

  /**
   * Delete a unit
   */
  const deleteUnit = async (name) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.delete_unit', { name })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to delete unit.' }
    }
  }

  /**
   * Get all users with their KRCS roles
   */
  const getUsers = async () => {
    try {
      const res = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_users')
      return res.data.message || []
    } catch {
      return []
    }
  }

  /**
   * Create a new user
   */
  const createUser = async (email, firstName, lastName, department, roles) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.create_user', {
        email,
        first_name: firstName,
        last_name: lastName,
        department: department || null,
        roles: JSON.stringify(roles)
      })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to create user.' }
    }
  }

  /**
   * Update a user's department and KRCS roles
   */
  const updateUser = async (user, department, roles) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.update_user', {
        user,
        department: department || null,
        roles: JSON.stringify(roles)
      })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to update user.' }
    }
  }

  /**
   * Update a user's KRCS roles (legacy - kept for compatibility)
   */
  const updateUserRoles = async (user, roles) => {
    return updateUser(user, null, roles)
  }

  /**
   * Enable/disable a user
   */
  const toggleUserEnabled = async (user, enabled) => {
    try {
      const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.toggle_user_enabled', {
        user,
        enabled: enabled ? 1 : 0
      })
      return res.data.message || { success: false }
    } catch (err) {
      return { success: false, message: err.response?.data?.message || 'Failed to toggle user.' }
    }
  }

  /**
   * Get admin metadata (roles list, is_system_manager check)
   */
  const getAdminMeta = async () => {
    try {
      const res = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_admin_meta')
      return res.data.message || { is_system_manager: false, krcs_roles: [] }
    } catch {
      return { is_system_manager: false, krcs_roles: [] }
    }
  }

  const getCurrentUser = async () => {
    try {
      const res = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_current_user')
      return res.data.message || null
    } catch (err) {
      console.error('Failed to get current user:', err)
      return null
    }
  }

  return {
    loading,
    error,
    fetchRisks,
    fetchRisk,
    getRiskStats,
    getRiskMatrix,
    addRiskReview,
    updateRiskReview,
    deleteRiskReview,
    getUserRoles,
    canApproveRisk,
    submitForApproval,
    requestClose,
    approveRisk,
    rejectRisk,
    // Admin APIs
    getDepartments,
    createDepartment,
    deleteDepartment,
    createUnit,
    deleteUnit,
    getUsers,
    createUser,
    updateUser,
    updateUserRoles,
    toggleUserEnabled,
    getAdminMeta,
    getCurrentUser,
  }
}
