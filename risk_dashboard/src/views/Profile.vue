<template>
  <div class="animate-fade-in">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-charcoal mb-2">My Profile</h1>
      <p class="text-medium-gray">View and manage your account information</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-primary"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card bg-red-50 border-red-200">
      <p class="text-red-600">{{ error }}</p>
    </div>

    <!-- Profile Content -->
    <div v-else-if="profile" class="space-y-6">
      <!-- Personal Information -->
      <div class="card">
        <h2 class="card-header">Personal Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Full Name</label>
            <p class="text-lg text-charcoal">{{ profile.full_name }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Email</label>
            <p class="text-lg text-charcoal">{{ profile.email }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Username</label>
            <p class="text-lg text-charcoal">{{ profile.username || 'Not set' }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Department</label>
            <p class="text-lg text-charcoal">{{ departmentName || 'Not assigned' }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">User Type</label>
            <p class="text-lg text-charcoal">{{ profile.user_type }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Language</label>
            <p class="text-lg text-charcoal">{{ profile.language || 'English' }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Time Zone</label>
            <p class="text-lg text-charcoal">{{ profile.time_zone || 'Not set' }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Last Login</label>
            <p class="text-lg text-charcoal">{{ formatDateTime(profile.last_login) }}</p>
          </div>
        </div>
      </div>

      <!-- KRCS Roles -->
      <div class="card">
        <h2 class="card-header">KRCS Roles</h2>
        <div v-if="krcsRoles.length > 0" class="flex flex-wrap gap-2">
          <span
            v-for="role in krcsRoles"
            :key="role"
            class="px-3 py-1.5 bg-red-primary text-white rounded-full text-sm font-medium"
          >
            {{ role }}
          </span>
        </div>
        <p v-else class="text-medium-gray">No KRCS roles assigned</p>
      </div>

      <!-- All System Roles -->
      <div class="card">
        <h2 class="card-header">System Roles</h2>
        <div v-if="profile.roles && profile.roles.length > 0" class="flex flex-wrap gap-2">
          <span
            v-for="role in profile.roles"
            :key="role.name"
            class="px-3 py-1.5 bg-light-gray text-charcoal rounded-full text-sm"
          >
            {{ role.role }}
          </span>
        </div>
        <p v-else class="text-medium-gray">No roles assigned</p>
      </div>

      <!-- Active Sessions -->
      <div class="card">
        <h2 class="card-header">Active Sessions</h2>
        <div v-if="profile.active_sessions && profile.active_sessions.length > 0" class="space-y-3">
          <div
            v-for="session in profile.active_sessions"
            :key="session.name"
            class="p-4 bg-light-gray rounded-lg"
            :class="{ 'border-2 border-red-primary': session.is_current }"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center space-x-2 mb-2">
                  <span class="font-semibold text-charcoal">{{ session.id }}</span>
                  <span
                    v-if="session.is_current"
                    class="px-2 py-0.5 bg-red-primary text-white rounded-full text-xs font-semibold"
                  >
                    Current Session
                  </span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-medium-gray">
                  <div>
                    <span class="font-medium">IP Address:</span> {{ session.ip_address }}
                  </div>
                  <div>
                    <span class="font-medium">Created:</span> {{ formatDateTime(session.session_created) }}
                  </div>
                  <div class="md:col-span-2">
                    <span class="font-medium">User Agent:</span> {{ session.user_agent }}
                  </div>
                  <div>
                    <span class="font-medium">Last Active:</span> {{ formatDateTime(session.last_updated) }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p v-else class="text-medium-gray">No active sessions</p>
      </div>

      <!-- Account Statistics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="card">
          <div class="flex items-center space-x-3">
            <div class="p-3 bg-red-light rounded-lg">
              <svg class="w-6 h-6 text-red-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-sm text-medium-gray">Member Since</p>
              <p class="text-lg font-semibold text-charcoal">{{ formatDate(profile.creation) }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center space-x-3">
            <div class="p-3 bg-blue-100 rounded-lg">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-sm text-medium-gray">Account Status</p>
              <p class="text-lg font-semibold" :class="profile.enabled ? 'text-green-600' : 'text-red-600'">
                {{ profile.enabled ? 'Active' : 'Disabled' }}
              </p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center space-x-3">
            <div class="p-3 bg-purple-100 rounded-lg">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div>
              <p class="text-sm text-medium-gray">Active Sessions</p>
              <p class="text-lg font-semibold text-charcoal">{{ profile.active_sessions?.length || 0 }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const error = ref('')
const profile = ref(null)
const departments = ref([])

const krcsRoles = computed(() => {
  if (!profile.value?.roles) return []
  return profile.value.roles
    .filter(r => r.role.startsWith('KRCS '))
    .map(r => r.role)
})

const departmentName = computed(() => {
  if (!profile.value?.krcs_department) return null
  const dept = departments.value.find(d => d.name === profile.value.krcs_department)
  return dept ? dept.department_name : profile.value.krcs_department
})

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadProfile = async () => {
  loading.value = true
  error.value = ''

  try {
    // Get current logged in user
    const userRes = await axios.get('/api/method/frappe.auth.get_logged_user')
    const username = userRes.data.message

    // Fetch full profile with all fields
    const profileRes = await axios.get(`/api/resource/User/${username}`, {
      params: {
        fields: JSON.stringify([
          'name', 'email', 'first_name', 'last_name', 'full_name', 'username',
          'krcs_department', 'user_type', 'language', 'time_zone', 'enabled',
          'creation', 'last_login', 'last_active', 'last_ip',
          'roles', 'active_sessions'
        ])
      }
    })
    profile.value = profileRes.data.data

    // Fetch departments
    const deptRes = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_departments')
    departments.value = deptRes.data.message || []
  } catch (err) {
    console.error('Failed to load profile:', err)
    error.value = 'Failed to load profile information. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>
