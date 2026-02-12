<template>
  <div class="animate-fade-in">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-charcoal mb-2">Risk Dashboard</h1>
      <p class="text-medium-gray">Overview of organizational risk exposure and management</p>
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
          :value="store.stats.total"
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
          :value="store.stats.critical"
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
          :value="store.stats.high"
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
          :value="store.stats.medium"
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
          :value="store.stats.low"
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
          :value="store.stats.overdue"
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
          :value="store.stats.dueSoon"
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
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-charcoal">Recent Risks</h2>
          <router-link to="/risks" class="btn btn-outline">
            View All Risks
          </router-link>
        </div>

        <div v-if="recentRisks.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <RiskCard
            v-for="risk in recentRisks"
            :key="risk.name"
            :risk="risk"
            @click="viewRisk(risk)"
          />
        </div>

        <div v-else class="card text-center py-12">
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRiskStore } from '../stores/riskStore'
import StatsCard from '../components/StatsCard.vue'
import RiskMatrix from '../components/RiskMatrix.vue'
import RiskCard from '../components/RiskCard.vue'

const store = useRiskStore()
const router = useRouter()
const selectedCell = ref(null)

const recentRisks = computed(() => {
  return store.risks.slice(0, 6)
})

const handleCellClick = ({ risks }) => {
  if (risks.length > 0) {
    selectedCell.value = { risks }
  }
}

const viewRisk = (risk) => {
  router.push(`/risk/${risk.name}`)
}

onMounted(() => {
  store.loadRisks()
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
