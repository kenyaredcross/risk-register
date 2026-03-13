<template>
  <div class="landing-page">
    <div class="header">
      <h1>KRCS Risk Management System</h1>
      <p class="subtitle">Welcome, {{ authStore.fullName }}</p>
    </div>

    <div class="services-container">
      <div v-if="hasRiskAccess" class="service-card" @click="navigateToRiskDashboard">
        <div class="service-icon risk-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
            <line x1="12" y1="9" x2="12" y2="13"></line>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
          </svg>
        </div>
        <h2>Risk Management</h2>
        <p>Manage program risks, view risk register, and track mitigation actions</p>
        <div class="service-actions">
          <span class="action-link">Go to Risk Dashboard →</span>
        </div>
      </div>

      <div class="service-card" @click="navigateToCOI">
        <div class="service-icon coi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
        </div>
        <h2>Conflict of Interest</h2>
        <p>Submit and manage your conflict of interest declarations</p>
        <div class="service-actions">
          <span class="action-link">Go to COI Declarations →</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// Check if user has any KRCS risk role
const hasRiskAccess = computed(() => {
  const riskRoles = ['KRCS HOR', 'KRCS DSG', 'KRCS HOD', 'KRCS Project Manager',
                     'KRCS RPC', 'KRCS Finance Officer', 'KRCS Procurement Manager',
                     'KRCS Logistics Manager', 'KRCS HR Manager', 'System Manager']
  return authStore.roles.some(role => riskRoles.includes(role))
})

const navigateToRiskDashboard = () => {
  router.push('/risk-dashboard/register-dash')
}

const navigateToCOI = () => {
  // Auditors and System Managers go to COI Dashboard
  if (authStore.isSystemManager || authStore.isAudit) {
    router.push('/risk-dashboard/coi-dashboard')
  } else {
    // Regular employees go to My page
    router.push('/my')
  }
}
</script>

<style scoped>
.landing-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.125rem;
  color: #6b7280;
}

.services-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.service-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.service-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
  border-color: #d73c3c;
}

.service-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.risk-icon {
  background: #fef2f2;
  color: #dc2626;
}

.coi-icon {
  background: #eff6ff;
  color: #2563eb;
}

.service-card h2 {
  font-size: 1.5rem;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.service-card p {
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.service-actions {
  margin-top: auto;
}

.action-link {
  color: #d73c3c;
  font-weight: 500;
  font-size: 0.875rem;
}

.service-card:hover .action-link {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .landing-page {
    padding: 1rem;
  }

  .header h1 {
    font-size: 1.5rem;
  }

  .services-container {
    grid-template-columns: 1fr;
  }
}
</style>
