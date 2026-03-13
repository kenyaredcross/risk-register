<template>
  <div class="coi-dashboard">
    <!-- Page Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-charcoal mb-2">Conflict of Interest Declarations</h1>
          <p class="text-medium-gray">Manage and review conflict of interest declarations for KRCS employees</p>
        </div>
        <router-link
          to="/coi-declaration/create"
          class="flex items-center space-x-2 bg-red-primary hover:bg-red-dark text-white px-6 py-3 rounded-lg transition-colors duration-200 font-medium shadow-sm hover:shadow-md"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>New Declaration</span>
        </router-link>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-sm border border-light-border p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-medium-gray mb-1">My Declarations</p>
            <p class="text-3xl font-bold text-charcoal">{{ stats.my_declarations }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-light-border p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-medium-gray mb-1">Pending Submissions</p>
            <p class="text-3xl font-bold text-orange-600">{{ stats.pending_submissions }}</p>
          </div>
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-light-border p-6" v-if="canReview">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-medium-gray mb-1">Pending Reviews</p>
            <p class="text-3xl font-bold text-yellow-600">{{ stats.pending_reviews }}</p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-light-border p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-medium-gray mb-1">Approved</p>
            <p class="text-3xl font-bold text-green-600">{{ stats.approved }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab Navigation - For Auditors/Reviewers Only -->
    <div class="bg-white rounded-lg shadow-sm border border-light-border mb-6">
      <div class="border-b border-light-border">
        <nav class="flex space-x-8 px-6" aria-label="Tabs">
          <button
            @click="activeTab = 'my'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === 'my'
                ? 'border-red-primary text-red-primary'
                : 'border-transparent text-medium-gray hover:text-charcoal hover:border-gray-300'
            ]"
          >
            My Declarations
          </button>
          <button
            @click="activeTab = 'pending'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === 'pending'
                ? 'border-red-primary text-red-primary'
                : 'border-transparent text-medium-gray hover:text-charcoal hover:border-gray-300'
            ]"
          >
            Pending Reviews
            <span v-if="stats.pending_reviews > 0" class="ml-2 bg-red-primary text-white text-xs font-bold px-2 py-0.5 rounded-full">
              {{ stats.pending_reviews }}
            </span>
          </button>
          <button
            @click="activeTab = 'all'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === 'all'
                ? 'border-red-primary text-red-primary'
                : 'border-transparent text-medium-gray hover:text-charcoal hover:border-gray-300'
            ]"
          >
            All Declarations
          </button>
        </nav>
      </div>

      <!-- Tab Content -->
      <div class="p-6">
        <!-- Filters -->
        <div class="mb-6 flex flex-wrap gap-4">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Status</label>
            <select v-model="filters.status" class="input w-48">
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
            <select v-model="filters.declaration_type" class="input w-48">
              <option value="">All Types</option>
              <option value="Annual Declaration">Annual Declaration</option>
              <option value="Change in Circumstance">Change in Circumstance</option>
            </select>
          </div>
          <div class="flex items-end">
            <button
              @click="loadDeclarations"
              class="btn-secondary"
            >
              Apply Filters
            </button>
          </div>
        </div>

        <!-- Table -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-red-primary"></div>
          <p class="text-medium-gray mt-4">Loading declarations...</p>
        </div>

        <div v-else-if="filteredDeclarations.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-medium-gray" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="text-medium-gray mt-4">No declarations found</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-light-border">
            <thead class="bg-light-gray">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Employee</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Department</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Type</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-medium-gray uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-medium-gray uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-light-border">
              <tr v-for="declaration in filteredDeclarations" :key="declaration.name" class="hover:bg-light-gray transition-colors">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-charcoal">{{ declaration.employee_name }}</div>
                  <div class="text-sm text-medium-gray">{{ declaration.employee }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-charcoal">{{ declaration.department || '-' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-charcoal">{{ declaration.declaration_type }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-charcoal">{{ formatDate(declaration.declaration_date) }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusClass(declaration.status)">
                    {{ declaration.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    @click="viewDeclaration(declaration)"
                    class="text-red-primary hover:text-red-dark"
                  >
                    View Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- View Declaration Modal -->
    <div v-if="selectedDeclaration" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="selectedDeclaration = null">
      <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div class="sticky top-0 bg-white border-b border-light-border px-6 py-4 flex items-center justify-between">
          <h3 class="text-xl font-bold text-charcoal">Declaration Details</h3>
          <button @click="selectedDeclaration = null" class="text-medium-gray hover:text-charcoal">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6">
          <!-- Declaration content -->
          <div class="space-y-6">
            <div>
              <h4 class="text-sm font-medium text-medium-gray mb-2">Employee Information</h4>
              <div class="bg-light-gray p-4 rounded-lg">
                <p class="text-sm"><span class="font-medium">Name:</span> {{ selectedDeclaration.employee_name }}</p>
                <p class="text-sm"><span class="font-medium">Department:</span> {{ selectedDeclaration.department || '-' }}</p>
                <p class="text-sm"><span class="font-medium">Designation:</span> {{ selectedDeclaration.designation || '-' }}</p>
              </div>
            </div>

            <div>
              <h4 class="text-sm font-medium text-medium-gray mb-2">Declaration Information</h4>
              <div class="bg-light-gray p-4 rounded-lg space-y-2">
                <p class="text-sm"><span class="font-medium">Type:</span> {{ selectedDeclaration.declaration_type }}</p>
                <p class="text-sm"><span class="font-medium">Date:</span> {{ formatDate(selectedDeclaration.declaration_date) }}</p>
                <p class="text-sm">
                  <span class="font-medium">Status:</span>
                  <span :class="getStatusClass(selectedDeclaration.status)" class="ml-2">
                    {{ selectedDeclaration.status }}
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import axios from 'axios'

const authStore = useAuthStore()
const loading = ref(false)
const stats = ref({
  my_declarations: 0,
  pending_submissions: 0,
  pending_reviews: 0,
  approved: 0,
  rejected: 0
})

const declarations = ref([])
const selectedDeclaration = ref(null)
const activeTab = ref('my')
const filters = ref({
  status: '',
  declaration_type: ''
})

const canReview = computed(() => {
  return authStore.isSystemManager || authStore.isAudit
})

const filteredDeclarations = computed(() => {
  let filtered = declarations.value

  if (activeTab.value === 'my') {
    // Filter to show only current user's declarations
    filtered = filtered.filter(d => d.employee === authStore.currentEmployee)
  } else if (activeTab.value === 'pending') {
    // Filter to show only submitted declarations
    filtered = filtered.filter(d => d.status === 'Submitted')
  }

  return filtered
})

const getStatusClass = (status) => {
  const classes = {
    'Draft': 'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800',
    'Submitted': 'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800',
    'Under Review': 'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800',
    'Approved': 'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800',
    'Rejected': 'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800'
  }
  return classes[status] || classes['Draft']
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

const loadStats = async () => {
  try {
    const response = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.conflict_of_interest_declaration.api.get_declaration_stats')
    stats.value = response.data.message || stats.value
  } catch (error) {
    console.error('Failed to load stats:', error)
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
    console.error('Failed to load declarations:', error)
  } finally {
    loading.value = false
  }
}

const viewDeclaration = (declaration) => {
  selectedDeclaration.value = declaration
}

onMounted(async () => {
  await loadStats()
  await loadDeclarations()
})
</script>

<style scoped>
.input {
  @apply w-full px-3 py-2 border border-light-border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-primary focus:border-transparent;
}

.btn-secondary {
  @apply px-4 py-2 border border-light-border rounded-lg text-charcoal hover:bg-light-gray transition-colors;
}
</style>
