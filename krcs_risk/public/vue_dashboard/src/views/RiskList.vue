<template>
  <div class="animate-fade-in">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-charcoal mb-2">Risk Register</h1>
      <p class="text-medium-gray">Complete list of identified risks across the organization</p>
    </div>

    <!-- Filters & Search -->
    <div class="card mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
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
      </div>

      <!-- Active Filters -->
      <div v-if="hasActiveFilters" class="mt-4 pt-4 border-t border-light-border flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <span class="text-sm text-medium-gray">Active filters:</span>
          <span v-if="filterLevel" class="badge badge-medium">{{ filterLevel }}</span>
          <span v-if="filterStatus" class="badge badge-medium">{{ filterStatus }}</span>
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
      <!-- Results Count -->
      <div class="mb-4 flex items-center justify-between">
        <p class="text-medium-gray">
          Showing <span class="font-semibold text-charcoal">{{ filteredRisks.length }}</span> of <span class="font-semibold text-charcoal">{{ store.risks.length }}</span> risks
        </p>

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

      <!-- Risks Grid -->
      <div v-if="filteredRisks.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <RiskCard
          v-for="risk in filteredRisks"
          :key="risk.name"
          :risk="risk"
          @click="viewRisk(risk)"
        />
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

const store = useRiskStore()
const router = useRouter()

const searchQuery = ref('')
const filterLevel = ref('')
const filterStatus = ref('')
const sortBy = ref('rating-desc')

const hasActiveFilters = computed(() => {
  return searchQuery.value || filterLevel.value || filterStatus.value
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

  // Risk level filter
  if (filterLevel.value) {
    risks = risks.filter(risk => risk.risk_level === filterLevel.value)
  }

  // Status filter
  if (filterStatus.value) {
    risks = risks.filter(risk => risk.status === filterStatus.value)
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
}

const viewRisk = (risk) => {
  router.push(`/risk/${risk.name}`)
}

onMounted(() => {
  if (store.risks.length === 0) {
    store.loadRisks()
  }
})
</script>
