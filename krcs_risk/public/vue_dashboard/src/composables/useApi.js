import { ref } from 'vue'
import axios from 'axios'

// Configure axios defaults
axios.defaults.baseURL = window.location.origin
axios.defaults.headers.common['X-Frappe-CSRF-Token'] = window.csrf_token || ''

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
            'risk_description',
            'likelihood',
            'impact',
            'overall_rating',
            'risk_level',
            'risk_owner',
            'department',
            'status',
            'timeline',
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

  return {
    loading,
    error,
    fetchRisks,
    fetchRisk,
    getRiskStats,
    getRiskMatrix,
    addRiskReview,
    updateRiskReview,
    deleteRiskReview
  }
}
