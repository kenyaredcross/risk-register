<template>
  <div class="animate-fade-in">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-charcoal mb-2">Risk Dashboard</h1>
      <p class="text-medium-gray">Overview of organizational risk exposure and management</p>
    </div>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Department Filter -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Filter by Department</label>
          <select v-model="filterDepartment" class="input">
            <option value="">All Departments</option>
            <option v-for="dept in departments" :key="dept.name" :value="dept.name">
              {{ dept.department_name }}
            </option>
          </select>
        </div>

        <!-- Unit Filter -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Filter by Unit</label>
          <select v-model="filterUnit" class="input" :disabled="!filterDepartment">
            <option value="">All Units</option>
            <option v-for="unit in filteredUnits" :key="unit.name" :value="unit.name">
              {{ unit.unit_name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Active Filters -->
      <div v-if="hasActiveFilters" class="mt-4 pt-4 border-t border-light-border flex items-center justify-between">
        <div class="flex items-center flex-wrap gap-2">
          <span class="text-sm text-medium-gray">Showing data for:</span>
          <span v-if="filterDepartment" class="badge badge-medium">{{ getDepartmentName(filterDepartment) }}</span>
          <span v-if="filterUnit" class="badge badge-medium">{{ getUnitName(filterUnit) }}</span>
        </div>
        <button @click="clearFilters" class="text-sm text-red-primary hover:text-red-hover font-medium">
          Clear Filters
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-primary"></div>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-7 gap-6 mb-8">
        <StatsCard
          :value="filteredStats.total"
          label="Total Risks"
          variant="default"
          :delay="0"
        >
          <template #icon>
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          :value="filteredStats.critical"
          label="Critical Risks"
          variant="critical"
          :delay="100"
        >
          <template #icon>
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          :value="filteredStats.high"
          label="High Risks"
          variant="high"
          :delay="200"
        >
          <template #icon>
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          :value="filteredStats.medium"
          label="Medium Risks"
          variant="medium"
          :delay="300"
        >
          <template #icon>
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          :value="filteredStats.low"
          label="Low Risks"
          variant="low"
          :delay="400"
        >
          <template #icon>
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          :value="filteredStats.overdue"
          label="Overdue Reviews"
          variant="critical"
          :delay="500"
        >
          <template #icon>
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          :value="filteredStats.dueSoon"
          label="Due Soon"
          variant="medium"
          :delay="600"
        >
          <template #icon>
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </template>
        </StatsCard>
      </div>

      <!-- Risk Matrix -->
      <div class="mb-8 animate-scale-in">
        <RiskMatrix
          :matrix="store.riskMatrix.matrix"
          :risks-by-cell="store.riskMatrix.risksByCell"
          @cell-click="handleCellClick"
        />
      </div>

      <!-- Recent Risks -->
      <div class="animate-slide-up">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <h2 class="text-2xl font-bold text-charcoal">Recent Risks</h2>
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
            <router-link to="/risks" class="btn btn-outline">
              View All Risks
            </router-link>
          </div>
        </div>

        <!-- Card View -->
        <div v-if="recentRisks.length > 0 && viewMode === 'card'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <RiskCard
            v-for="risk in recentRisks"
            :key="risk.name"
            :risk="risk"
            @click="viewRisk(risk)"
          />
        </div>

        <!-- Table View -->
        <div v-if="recentRisks.length > 0 && viewMode === 'table'" class="card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-light-gray">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Risk ID</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Description</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Department</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Risk Level</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Rating</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Owner</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Status</th>
                  <th class="px-4 py-3 text-right text-xs font-semibold text-charcoal uppercase">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-light-border">
                <tr v-for="risk in recentRisks" :key="risk.name" class="hover:bg-off-white transition-colors">
                  <td class="px-4 py-3 text-sm font-medium text-charcoal">
                    {{ risk.name }}
                  </td>
                  <td class="px-4 py-3 text-sm text-medium-gray">
                    <div class="line-clamp-2">{{ risk.risk_description }}</div>
                  </td>
                  <td class="px-4 py-3 text-sm text-medium-gray">
                    {{ risk.department || '-' }}
                  </td>
                  <td class="px-4 py-3">
                    <span
                      class="px-2 py-1 rounded-full text-xs font-semibold"
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
                      class="px-2 py-1 rounded-full text-xs font-semibold"
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

        <div v-if="recentRisks.length === 0" class="card text-center py-12">
          <svg class="w-16 h-16 text-medium-gray mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="text-medium-gray">No risks found in the system</p>
        </div>
      </div>
    </div>

    <!-- Cell Click Modal (Simple) -->
    <div v-if="selectedCell" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click="selectedCell = null">
      <div class="bg-white rounded-lg shadow-elegant-xl max-w-2xl w-full max-h-96 overflow-y-auto p-6" @click.stop>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-bold text-charcoal">Risks in Cell ({{ selectedCell.risks.length }})</h3>
          <button @click="selectedCell = null" class="text-medium-gray hover:text-charcoal">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-3">
          <div
            v-for="risk in selectedCell.risks"
            :key="risk.name"
            class="p-3 border border-light-border rounded-lg hover:bg-light-gray cursor-pointer"
            @click="viewRisk(risk)"
          >
            <div class="font-semibold text-charcoal">{{ risk.name }}</div>
            <div class="text-sm text-medium-gray line-clamp-1">{{ risk.risk_description }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useRiskStore } from '../stores/riskStore'
import StatsCard from '../components/StatsCard.vue'
import RiskMatrix from '../components/RiskMatrix.vue'
import RiskCard from '../components/RiskCard.vue'
import axios from 'axios'

const store = useRiskStore()
const router = useRouter()
const selectedCell = ref(null)
const viewMode = ref('card') // 'card' or 'table'

const filterDepartment = ref('')
const filterUnit = ref('')
const departments = ref([])
const allUnits = ref([])

const hasActiveFilters = computed(() => {
  return filterDepartment.value || filterUnit.value
})

const filteredUnits = computed(() => {
  if (!filterDepartment.value) return []
  return allUnits.value.filter(u => u.department === filterDepartment.value)
})

// Watch department changes to clear unit filter
watch(filterDepartment, () => {
  if (filterUnit.value) {
    const unitBelongsToDept = filteredUnits.value.some(u => u.name === filterUnit.value)
    if (!unitBelongsToDept) {
      filterUnit.value = ''
    }
  }
})

const filteredRisks = computed(() => {
  let risks = [...store.risks]

  if (filterDepartment.value) {
    risks = risks.filter(risk => risk.department === filterDepartment.value)
  }

  if (filterUnit.value) {
    risks = risks.filter(risk => risk.unit === filterUnit.value)
  }

  return risks
})

const filteredStats = computed(() => {
  const risks = filteredRisks.value

  return {
    total: risks.length,
    critical: risks.filter(r => r.risk_level === 'Critical').length,
    high: risks.filter(r => r.risk_level === 'High').length,
    medium: risks.filter(r => r.risk_level === 'Medium').length,
    low: risks.filter(r => r.risk_level === 'Low').length,
    overdue: risks.filter(r => r.review_status === 'Overdue').length,
    dueSoon: risks.filter(r => r.review_status === 'Due Soon').length,
  }
})

const recentRisks = computed(() => {
  return filteredRisks.value.slice(0, 6)
})

const handleCellClick = ({ risks }) => {
  if (risks.length > 0) {
    selectedCell.value = { risks }
  }
}

const viewRisk = (risk) => {
  router.push(`/risk/${risk.name}`)
}

const clearFilters = () => {
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

onMounted(() => {
  store.loadRisks()
  loadDepartmentsAndUnits()
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
