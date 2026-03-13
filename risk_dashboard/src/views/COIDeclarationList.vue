<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-charcoal mb-2">Conflict of Interest Declarations</h1>
        <p class="text-medium-gray">View and manage your declarations</p>
      </div>
      <router-link to="/coi-declaration/create" class="btn btn-primary">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        New Declaration
      </router-link>
    </div>

    <!-- Statistics Cards (if user has declarations) -->
    <div v-if="stats" class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="card p-6">
        <div class="text-sm text-medium-gray mb-1">Total Declarations</div>
        <div class="text-3xl font-bold text-charcoal">{{ stats.my_declarations }}</div>
      </div>
      <div class="card p-6">
        <div class="text-sm text-medium-gray mb-1">Pending Submissions</div>
        <div class="text-3xl font-bold text-orange-600">{{ stats.pending_submissions }}</div>
      </div>
      <div class="card p-6">
        <div class="text-sm text-medium-gray mb-1">Approved</div>
        <div class="text-3xl font-bold text-green-600">{{ stats.approved }}</div>
      </div>
      <div class="card p-6" v-if="canReview">
        <div class="text-sm text-medium-gray mb-1">Pending Reviews</div>
        <div class="text-3xl font-bold text-red-primary">{{ stats.pending_reviews }}</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow-elegant p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Status</label>
          <select v-model="filters.status" @change="loadDeclarations" class="input">
            <option value="">All Statuses</option>
            <option value="Draft">Draft</option>
            <option value="Submitted">Submitted</option>
            <option value="Under Review">Under Review</option>
            <option value="Approved">Approved</option>
            <option value="Rejected">Rejected</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Declaration Type</label>
          <select v-model="filters.declaration_type" @change="loadDeclarations" class="input">
            <option value="">All Types</option>
            <option value="Annual Declaration">Annual Declaration</option>
            <option value="Change in Circumstance">Change in Circumstance</option>
          </select>
        </div>
        <div class="flex items-end">
          <button @click="resetFilters" class="btn btn-outline w-full">
            Reset Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Declarations Table -->
    <div class="bg-white rounded-lg shadow-elegant overflow-hidden">
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-red-primary border-t-transparent"></div>
        <p class="mt-2 text-medium-gray">Loading declarations...</p>
      </div>

      <div v-else-if="declarations.length === 0" class="p-8 text-center">
        <svg class="w-16 h-16 mx-auto text-light-gray mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-lg text-medium-gray mb-4">No declarations found</p>
        <router-link to="/coi-declaration/create" class="btn btn-primary">
          Create Your First Declaration
        </router-link>
      </div>

      <table v-else class="w-full">
        <thead class="bg-gray-50 border-b border-light-border">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Employee</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Department</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Type</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-light-border">
          <tr v-for="declaration in declarations" :key="declaration.name" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-charcoal">{{ declaration.employee_name }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-medium-gray">{{ declaration.department || 'N/A' }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-medium-gray">{{ declaration.declaration_type }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-medium-gray">{{ formatDate(declaration.declaration_date) }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getStatusBadgeClass(declaration.status)" class="px-2 py-1 text-xs font-semibold rounded-full">
                {{ declaration.status }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button
                @click="viewDeclaration(declaration)"
                class="text-red-primary hover:text-red-dark font-medium"
              >
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- View Declaration Modal -->
    <div v-if="showDetailModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="closeDetailModal">
      <div class="bg-white rounded-lg shadow-elegant-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto animate-scale-in">
        <!-- Modal Header -->
        <div class="sticky top-0 bg-white border-b border-light-border px-6 py-4 flex items-center justify-between">
          <h2 class="text-xl font-bold text-charcoal">Declaration Details</h2>
          <button @click="closeDetailModal" class="text-medium-gray hover:text-charcoal">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Modal Content -->
        <div v-if="selectedDeclaration" class="p-6 space-y-6">
          <!-- Basic Info -->
          <div>
            <h3 class="text-lg font-semibold text-charcoal mb-4">Basic Information</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <div class="text-sm text-medium-gray">Employee Name</div>
                <div class="font-medium">{{ selectedDeclaration.employee_name }}</div>
              </div>
              <div>
                <div class="text-sm text-medium-gray">Department</div>
                <div class="font-medium">{{ selectedDeclaration.department || 'N/A' }}</div>
              </div>
              <div>
                <div class="text-sm text-medium-gray">Declaration Type</div>
                <div class="font-medium">{{ selectedDeclaration.declaration_type }}</div>
              </div>
              <div>
                <div class="text-sm text-medium-gray">Declaration Date</div>
                <div class="font-medium">{{ formatDate(selectedDeclaration.declaration_date) }}</div>
              </div>
              <div>
                <div class="text-sm text-medium-gray">Status</div>
                <span :class="getStatusBadgeClass(selectedDeclaration.status)" class="px-2 py-1 text-xs font-semibold rounded-full">
                  {{ selectedDeclaration.status }}
                </span>
              </div>
            </div>
          </div>

          <!-- Declarations -->
          <div class="space-y-4">
            <div class="border-t border-light-border pt-4">
              <h4 class="font-semibold text-charcoal mb-2">Financial Interests</h4>
              <p class="text-sm text-medium-gray">{{ selectedDeclaration.has_financial_interests }}</p>
              <p v-if="selectedDeclaration.financial_interests_description" class="text-sm mt-2 p-3 bg-gray-50 rounded">
                {{ selectedDeclaration.financial_interests_description }}
              </p>
            </div>

            <div class="border-t border-light-border pt-4">
              <h4 class="font-semibold text-charcoal mb-2">Personal Relationships</h4>
              <p class="text-sm text-medium-gray">{{ selectedDeclaration.has_personal_relationships }}</p>
              <p v-if="selectedDeclaration.personal_relationships_description" class="text-sm mt-2 p-3 bg-gray-50 rounded">
                {{ selectedDeclaration.personal_relationships_description }}
              </p>
            </div>

            <div class="border-t border-light-border pt-4">
              <h4 class="font-semibold text-charcoal mb-2">Supervisory Roles</h4>
              <p class="text-sm text-medium-gray">{{ selectedDeclaration.has_supervisory_roles }}</p>
              <p v-if="selectedDeclaration.supervisory_roles_description" class="text-sm mt-2 p-3 bg-gray-50 rounded">
                {{ selectedDeclaration.supervisory_roles_description }}
              </p>
            </div>

            <div class="border-t border-light-border pt-4">
              <h4 class="font-semibold text-charcoal mb-2">Other Organizational Roles</h4>
              <p class="text-sm text-medium-gray">{{ selectedDeclaration.has_other_roles }}</p>
              <p v-if="selectedDeclaration.other_roles_description" class="text-sm mt-2 p-3 bg-gray-50 rounded">
                {{ selectedDeclaration.other_roles_description }}
              </p>
            </div>

            <div class="border-t border-light-border pt-4">
              <h4 class="font-semibold text-charcoal mb-2">Public Office Plans</h4>
              <p class="text-sm text-medium-gray">{{ selectedDeclaration.plans_public_office }}</p>
              <p v-if="selectedDeclaration.public_office_description" class="text-sm mt-2 p-3 bg-gray-50 rounded">
                {{ selectedDeclaration.public_office_description }}
              </p>
            </div>
          </div>

          <!-- Review Section (if reviewed) -->
          <div v-if="selectedDeclaration.review_comments" class="border-t border-light-border pt-4">
            <h3 class="text-lg font-semibold text-charcoal mb-4">Review</h3>
            <div class="bg-gray-50 p-4 rounded">
              <p class="text-sm text-medium-gray">{{ selectedDeclaration.review_comments }}</p>
              <div class="mt-2 text-xs text-medium-gray">
                Reviewed by {{ selectedDeclaration.reviewed_by || selectedDeclaration.approved_by }} on {{ formatDate(selectedDeclaration.review_date || selectedDeclaration.approval_date) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="sticky bottom-0 bg-gray-50 border-t border-light-border px-6 py-4 flex items-center justify-end">
          <button @click="closeDetailModal" class="btn btn-outline">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const declarations = ref([])
const stats = ref(null)
const loading = ref(false)
const showDetailModal = ref(false)
const selectedDeclaration = ref(null)

const filters = ref({
  status: '',
  declaration_type: ''
})

const canReview = computed(() => {
  return authStore.isSystemManager || authStore.isHOD || authStore.isHOR
})

const loadStats = async () => {
  try {
    const response = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.conflict_of_interest_declaration.api.get_declaration_stats')
    stats.value = response.data.message
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

const loadDeclarations = async () => {
  loading.value = true
  try {
    const filterParams = {}
    if (filters.value.status) filterParams.status = filters.value.status
    if (filters.value.declaration_type) filterParams.declaration_type = filters.value.declaration_type

    const response = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.conflict_of_interest_declaration.api.get_all_declarations', {
      params: { filters: JSON.stringify(filterParams) }
    })
    declarations.value = response.data.message || []
  } catch (error) {
    console.error('Error loading declarations:', error)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    status: '',
    declaration_type: ''
  }
  loadDeclarations()
}

const viewDeclaration = async (declaration) => {
  try {
    const response = await axios.get(`/api/method/krcs_risk.krcs_risk_management.doctype.conflict_of_interest_declaration.api.get_declaration`, {
      params: { name: declaration.name }
    })
    selectedDeclaration.value = response.data.message
    showDetailModal.value = true
  } catch (error) {
    console.error('Error loading declaration details:', error)
  }
}

const closeDetailModal = () => {
  showDetailModal.value = false
  selectedDeclaration.value = null
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getStatusBadgeClass = (status) => {
  const classes = {
    'Draft': 'bg-gray-100 text-gray-700',
    'Submitted': 'bg-blue-100 text-blue-700',
    'Under Review': 'bg-orange-100 text-orange-700',
    'Approved': 'bg-green-100 text-green-700',
    'Rejected': 'bg-red-100 text-red-700'
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

onMounted(() => {
  loadStats()
  loadDeclarations()
})
</script>
