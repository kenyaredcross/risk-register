<template>
  <div class="my-coi-page">
    <div class="page-header">
      <h1>My COI Declarations</h1>
      <button @click="createDeclaration" class="btn-primary">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        New Declaration
      </button>
    </div>

    <div v-if="loading" class="loading">Loading your declarations...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else>
      <div v-if="declarations.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
        </svg>
        <h3>No declarations yet</h3>
        <p>Click "New Declaration" above to submit your first conflict of interest declaration.</p>
      </div>

      <div v-else class="declarations-list">
        <div v-for="declaration in declarations" :key="declaration.name" class="declaration-card">
          <div class="declaration-header">
            <div class="declaration-title">
              <h3>{{ declaration.declaration_type }}</h3>
              <span class="declaration-date">{{ formatDate(declaration.declaration_date) }}</span>
            </div>
            <span :class="['status-badge', statusClass(declaration.status)]">
              {{ declaration.status }}
            </span>
          </div>

          <div class="declaration-details">
            <div v-if="declaration.employee_number" class="detail-row">
              <span class="detail-label">Employee Number:</span>
              <span class="detail-value">{{ declaration.employee_number }}</span>
            </div>
            <div v-if="declaration.designation" class="detail-row">
              <span class="detail-label">Designation:</span>
              <span class="detail-value">{{ declaration.designation }}</span>
            </div>
            <div v-if="declaration.department" class="detail-row">
              <span class="detail-label">Department:</span>
              <span class="detail-value">{{ declaration.department }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Submitted:</span>
              <span class="detail-value">{{ formatDate(declaration.creation) }}</span>
            </div>
            <div v-if="declaration.reviewed_by" class="detail-row">
              <span class="detail-label">Reviewed by:</span>
              <span class="detail-value">{{ declaration.reviewed_by }}</span>
            </div>
            <div v-if="declaration.review_comments" class="detail-row">
              <span class="detail-label">Comments:</span>
              <span class="detail-value">{{ declaration.review_comments }}</span>
            </div>
          </div>

          <div class="declaration-actions">
            <button @click="viewDeclaration(declaration.name)" class="btn-link">
              View Details →
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const declarations = ref([])
const loading = ref(true)
const error = ref(null)

const fetchMyDeclarations = async () => {
  try {
    loading.value = true
    const response = await axios.get(
      '/api/method/krcs_risk.krcs_risk_management.doctype.conflict_of_interest_declaration.api.get_my_declarations'
    )
    declarations.value = response.data.message || []
  } catch (err) {
    error.value = 'Failed to load declarations. Please try again.'
    console.error('Error fetching declarations:', err)
  } finally {
    loading.value = false
  }
}

const createDeclaration = () => {
  router.push('/coi-declaration/create')
}

const viewDeclaration = (name) => {
  router.push(`/coi-declaration/${name}`)
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const statusClass = (status) => {
  const statusMap = {
    'Draft': 'status-draft',
    'Submitted': 'status-submitted',
    'Under Review': 'status-review',
    'Approved': 'status-approved',
    'Rejected': 'status-rejected'
  }
  return statusMap[status] || 'status-draft'
}

onMounted(() => {
  fetchMyDeclarations()
})
</script>

<style scoped>
.my-coi-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 1.875rem;
  color: #1f2937;
  margin: 0;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #d73c3c;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #b91c1c;
}

.loading, .error-message {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;
}

.error-message {
  color: #dc2626;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6b7280;
}

.empty-state svg {
  margin: 0 auto 1.5rem;
  color: #d1d5db;
}

.empty-state h3 {
  font-size: 1.25rem;
  color: #374151;
  margin-bottom: 0.5rem;
}

.empty-state p {
  font-size: 0.875rem;
}

.declarations-list {
  display: grid;
  gap: 1rem;
}

.declaration-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  transition: box-shadow 0.2s;
}

.declaration-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.declaration-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.declaration-title h3 {
  font-size: 1.125rem;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.declaration-date {
  font-size: 0.875rem;
  color: #6b7280;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-draft {
  background-color: #f3f4f6;
  color: #374151;
}

.status-submitted {
  background-color: #dbeafe;
  color: #1e40af;
}

.status-review {
  background-color: #fef3c7;
  color: #92400e;
}

.status-approved {
  background-color: #d1fae5;
  color: #065f46;
}

.status-rejected {
  background-color: #fee2e2;
  color: #991b1b;
}

.declaration-details {
  display: grid;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  font-size: 0.875rem;
}

.detail-label {
  font-weight: 500;
  color: #6b7280;
  min-width: 120px;
}

.detail-value {
  color: #1f2937;
}

.declaration-actions {
  border-top: 1px solid #f3f4f6;
  padding-top: 1rem;
  margin-top: 1rem;
}

.btn-link {
  background: none;
  border: none;
  color: #d73c3c;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  padding: 0;
}

.btn-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .my-coi-page {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
  }
}
</style>
