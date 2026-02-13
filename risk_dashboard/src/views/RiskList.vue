<template>
  <div class="animate-fade-in">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-charcoal mb-2">Risk Register</h1>
      <p class="text-medium-gray">Complete list of identified risks across the organization</p>
    </div>

    <!-- Filters & Search -->
    <div class="card mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-4">
        <!-- Search -->
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-charcoal mb-2">Search</label>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search risks..."
            class="input"
          />
        </div>

        <!-- Department Filter -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Department</label>
          <select v-model="filterDepartment" class="input">
            <option value="">All Departments</option>
            <option v-for="dept in departments" :key="dept.name" :value="dept.name">
              {{ dept.department_name }}
            </option>
          </select>
        </div>

        <!-- Unit Filter -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Unit</label>
          <select v-model="filterUnit" class="input" :disabled="!filterDepartment">
            <option value="">All Units</option>
            <option v-for="unit in filteredUnits" :key="unit.name" :value="unit.name">
              {{ unit.unit_name }}
            </option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Risk Level Filter -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Risk Level</label>
          <select v-model="filterLevel" class="input">
            <option value="">All Levels</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>

        <!-- Status Filter -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Status</label>
          <select v-model="filterStatus" class="input">
            <option value="">All Status</option>
            <option value="Open">Open</option>
            <option value="In Progress">In Progress</option>
            <option value="Closed">Closed</option>
            <option value="Mitigated">Mitigated</option>
          </select>
        </div>

        <!-- Review Status Filter -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Review Status</label>
          <select v-model="filterReviewStatus" class="input">
            <option value="">All Reviews</option>
            <option value="Overdue">🔴 Overdue</option>
            <option value="Due Soon">🟡 Due Soon</option>
            <option value="On Track">🟢 On Track</option>
            <option value="Not Scheduled">⚪ Not Scheduled</option>
          </select>
        </div>
      </div>

      <!-- Active Filters -->
      <div v-if="hasActiveFilters" class="mt-4 pt-4 border-t border-light-border flex items-center justify-between">
        <div class="flex items-center flex-wrap gap-2">
          <span class="text-sm text-medium-gray">Active filters:</span>
          <span v-if="filterDepartment" class="badge badge-medium">Dept: {{ getDepartmentName(filterDepartment) }}</span>
          <span v-if="filterUnit" class="badge badge-medium">Unit: {{ getUnitName(filterUnit) }}</span>
          <span v-if="filterLevel" class="badge badge-medium">{{ filterLevel }}</span>
          <span v-if="filterStatus" class="badge badge-medium">{{ filterStatus }}</span>
          <span v-if="filterReviewStatus" class="badge badge-medium">{{ filterReviewStatus }}</span>
        </div>
        <button @click="clearFilters" class="text-sm text-red-primary hover:text-red-hover font-medium">
          Clear All
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-primary"></div>
    </div>

    <!-- Risk List -->
    <div v-else>
      <!-- Results Count & Controls -->
      <div class="mb-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <p class="text-medium-gray">
          Showing <span class="font-semibold text-charcoal">{{ filteredRisks.length }}</span> of <span class="font-semibold text-charcoal">{{ store.risks.length }}</span> risks
        </p>

        <div class="flex flex-wrap items-center gap-3">
          <!-- View Toggle -->
          <div class="inline-flex items-center bg-light-gray rounded-lg p-1 border border-light-border">
            <button
              type="button"
              @click="viewMode = 'card'"
              :class="viewMode === 'card' ? 'bg-white shadow text-charcoal' : 'text-medium-gray hover:text-charcoal hover:bg-white/50'"
              class="inline-flex items-center px-3 py-1.5 rounded-md transition-all text-sm font-medium"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
              Cards
            </button>
            <button
              type="button"
              @click="viewMode = 'table'"
              :class="viewMode === 'table' ? 'bg-white shadow text-charcoal' : 'text-medium-gray hover:text-charcoal hover:bg-white/50'"
              class="inline-flex items-center px-3 py-1.5 rounded-md transition-all text-sm font-medium"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Table
            </button>
          </div>

          <!-- Sort -->
          <div class="flex items-center space-x-2">
            <label class="text-sm text-medium-gray">Sort by:</label>
            <select v-model="sortBy" class="text-sm border border-light-border rounded px-2 py-1 focus:outline-none focus:border-charcoal">
              <option value="rating-desc">Rating (High to Low)</option>
              <option value="rating-asc">Rating (Low to High)</option>
              <option value="date-desc">Date (Newest)</option>
              <option value="date-asc">Date (Oldest)</option>
              <option value="name">Name</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Card View -->
      <div v-if="filteredRisks.length > 0 && viewMode === 'card'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <RiskCard
          v-for="risk in filteredRisks"
          :key="risk.name"
          :risk="risk"
          @click="viewRisk(risk)"
        />
      </div>

      <!-- Table View -->
      <div v-if="filteredRisks.length > 0 && viewMode === 'table'" class="card overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-light-gray">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Risk ID</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Description</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Department</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Unit</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Risk Level</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Rating</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Owner</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Status</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Review Status</th>
                <th class="px-4 py-3 text-right text-xs font-semibold text-charcoal uppercase">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-light-border">
              <tr v-for="risk in filteredRisks" :key="risk.name" class="hover:bg-off-white transition-colors">
                <td class="px-4 py-3 text-sm font-medium text-charcoal">
                  {{ risk.name }}
                </td>
                <td class="px-4 py-3 text-sm text-medium-gray max-w-xs">
                  <div class="line-clamp-2">{{ risk.risk_description }}</div>
                </td>
                <td class="px-4 py-3 text-sm text-medium-gray">
                  {{ risk.department || '-' }}
                </td>
                <td class="px-4 py-3 text-sm text-medium-gray">
                  {{ risk.unit || '-' }}
                </td>
                <td class="px-4 py-3">
                  <span
                    class="px-2 py-1 rounded-full text-xs font-semibold whitespace-nowrap"
                    :class="{
                      'bg-critical-light text-critical-dark': risk.risk_level === 'Critical',
                      'bg-high-light text-high-dark': risk.risk_level === 'High',
                      'bg-medium-light text-medium-dark': risk.risk_level === 'Medium',
                      'bg-low-light text-low-dark': risk.risk_level === 'Low'
                    }"
                  >
                    {{ risk.risk_level }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm font-medium text-charcoal">
                  {{ risk.overall_rating || '-' }}
                </td>
                <td class="px-4 py-3 text-sm text-medium-gray">
                  {{ risk.risk_owner || '-' }}
                </td>
                <td class="px-4 py-3">
                  <span
                    class="px-2 py-1 rounded-full text-xs font-semibold whitespace-nowrap"
                    :class="{
                      'bg-green-100 text-green-700': risk.status === 'Open',
                      'bg-blue-100 text-blue-700': risk.status === 'In Progress',
                      'bg-gray-100 text-gray-600': risk.status === 'Closed',
                      'bg-purple-100 text-purple-700': risk.status === 'Mitigated'
                    }"
                  >
                    {{ risk.status }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm">
                  <span v-if="risk.review_status === 'Overdue'" class="text-red-600">🔴 Overdue</span>
                  <span v-else-if="risk.review_status === 'Due Soon'" class="text-yellow-600">🟡 Due Soon</span>
                  <span v-else-if="risk.review_status === 'On Track'" class="text-green-600">🟢 On Track</span>
                  <span v-else class="text-medium-gray">⚪ Not Scheduled</span>
                </td>
                <td class="px-4 py-3 text-right">
                  <button
                    @click="viewRisk(risk)"
                    class="text-sm text-red-primary hover:text-red-dark font-medium"
                  >
                    View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="card text-center py-12">
        <svg class="w-16 h-16 text-medium-gray mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <p class="text-medium-gray mb-2">No risks found matching your criteria</p>
        <button @click="clearFilters" class="text-red-primary hover:text-red-hover font-medium">
          Clear filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRiskStore } from '../stores/riskStore'
import RiskCard from '../components/RiskCard.vue'
import axios from 'axios'

const store = useRiskStore()
const router = useRouter()

const searchQuery = ref('')
const filterLevel = ref('')
const filterStatus = ref('')
const filterReviewStatus = ref('')
const filterDepartment = ref('')
const filterUnit = ref('')
const sortBy = ref('rating-desc')
const viewMode = ref('card') // 'card' or 'table'

const departments = ref([])
const allUnits = ref([])

const hasActiveFilters = computed(() => {
  return searchQuery.value || filterLevel.value || filterStatus.value || filterReviewStatus.value || filterDepartment.value || filterUnit.value
})

const filteredUnits = computed(() => {
  if (!filterDepartment.value) return []
  return allUnits.value.filter(u => u.department === filterDepartment.value)
})

const filteredRisks = computed(() => {
  let risks = [...store.risks]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    risks = risks.filter(risk =>
      (risk.name || '').toLowerCase().includes(query) ||
      (risk.risk_description || '').toLowerCase().includes(query) ||
      (risk.risk_owner || '').toLowerCase().includes(query) ||
      (risk.department || '').toLowerCase().includes(query)
    )
  }

  // Department filter
  if (filterDepartment.value) {
    risks = risks.filter(risk => risk.department === filterDepartment.value)
  }

  // Unit filter
  if (filterUnit.value) {
    risks = risks.filter(risk => risk.unit === filterUnit.value)
  }

  // Risk level filter
  if (filterLevel.value) {
    risks = risks.filter(risk => risk.risk_level === filterLevel.value)
  }

  // Status filter
  if (filterStatus.value) {
    risks = risks.filter(risk => risk.status === filterStatus.value)
  }

  // Review status filter
  if (filterReviewStatus.value) {
    risks = risks.filter(risk => (risk.review_status || 'Not Scheduled') === filterReviewStatus.value)
  }

  // Sort
  risks.sort((a, b) => {
    switch (sortBy.value) {
      case 'rating-desc':
        return (b.overall_rating || 0) - (a.overall_rating || 0)
      case 'rating-asc':
        return (a.overall_rating || 0) - (b.overall_rating || 0)
      case 'date-desc':
        return new Date(b.creation || 0) - new Date(a.creation || 0)
      case 'date-asc':
        return new Date(a.creation || 0) - new Date(b.creation || 0)
      case 'name':
        return (a.name || '').localeCompare(b.name || '')
      default:
        return 0
    }
  })

  return risks
})

const clearFilters = () => {
  searchQuery.value = ''
  filterLevel.value = ''
  filterStatus.value = ''
  filterReviewStatus.value = ''
  filterDepartment.value = ''
  filterUnit.value = ''
}

const getDepartmentName = (deptId) => {
  const dept = departments.value.find(d => d.name === deptId)
  return dept ? dept.department_name : deptId
}

const getUnitName = (unitId) => {
  const unit = allUnits.value.find(u => u.name === unitId)
  return unit ? unit.unit_name : unitId
}

const loadDepartmentsAndUnits = async () => {
  try {
    const res = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_departments')
    const depts = res.data.message || []
    departments.value = depts
    allUnits.value = depts.flatMap(d => d.units || [])
  } catch (err) {
    console.error('Failed to load departments and units', err)
  }
}

const viewRisk = (risk) => {
  router.push(`/risk/${risk.name}`)
}

onMounted(() => {
  if (store.risks.length === 0) {
    store.loadRisks()
  }
  loadDepartmentsAndUnits()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
