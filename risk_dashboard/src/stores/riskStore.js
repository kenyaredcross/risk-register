import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '../composables/useApi'

export const useRiskStore = defineStore('risk', () => {
  const api = useApi()
  const risks = ref([])
  const selectedRisk = ref(null)
  const loading = ref(false)

  // Computed
  const stats = computed(() => api.getRiskStats(risks.value))
  const riskMatrix = computed(() => api.getRiskMatrix(risks.value))

  // Actions
  async function loadRisks() {
    loading.value = true
    risks.value = await api.fetchRisks()
    loading.value = false
  }

  async function loadRisk(name) {
    loading.value = true
    selectedRisk.value = await api.fetchRisk(name)
    loading.value = false
  }

  return {
    risks,
    selectedRisk,
    loading,
    stats,
    riskMatrix,
    loadRisks,
    loadRisk
  }
})
