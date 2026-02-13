<template>
  <div class="animate-fade-in">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-charcoal mb-2">Administration</h1>
      <p class="text-medium-gray">Manage departments, users, and roles</p>
    </div>

    <!-- Admin Navigation Tabs -->
    <div class="mb-6 border-b border-light-border">
      <nav class="flex space-x-6">
        <router-link
          to="/admin/departments"
          class="pb-3 px-1 border-b-2 font-medium text-sm transition-colors"
          :class="$route.path === '/admin/departments' ? 'border-red-primary text-red-primary' : 'border-transparent text-medium-gray hover:text-charcoal hover:border-light-border'"
        >
          Departments & Units
        </router-link>
        <router-link
          to="/admin/users"
          class="pb-3 px-1 border-b-2 font-medium text-sm transition-colors"
          :class="$route.path === '/admin/users' ? 'border-red-primary text-red-primary' : 'border-transparent text-medium-gray hover:text-charcoal hover:border-light-border'"
        >
          Users
        </router-link>
        <router-link
          to="/admin/roles"
          class="pb-3 px-1 border-b-2 font-medium text-sm transition-colors"
          :class="$route.path === '/admin/roles' ? 'border-red-primary text-red-primary' : 'border-transparent text-medium-gray hover:text-charcoal hover:border-light-border'"
        >
          Roles Reference
        </router-link>
      </nav>
    </div>

    <div class="mb-6 flex items-center justify-between">
      <div>
        <h2 class="text-xl font-bold text-charcoal mb-1">User Management</h2>
        <p class="text-sm text-medium-gray">Manage users and their KRCS roles</p>
      </div>
      <button @click="showCreateModal = true" class="btn btn-primary">
        <svg class="w-5 h-5 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add User
      </button>
    </div>

    <!-- Users List -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-primary"></div>
    </div>

    <div v-else class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-light-gray">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Name</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Email</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Department</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">Status</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-charcoal uppercase">KRCS Roles</th>
              <th class="px-4 py-3 text-right text-xs font-semibold text-charcoal uppercase">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-light-border">
            <tr v-for="user in users" :key="user.name" class="hover:bg-off-white transition-colors">
              <td class="px-4 py-3 text-sm text-charcoal font-medium">{{ user.full_name || user.name }}</td>
              <td class="px-4 py-3 text-sm text-medium-gray">{{ user.email }}</td>
              <td class="px-4 py-3 text-sm text-medium-gray">{{ user.department_name || '-' }}</td>
              <td class="px-4 py-3">
                <span
                  class="px-2 py-1 rounded-full text-xs font-semibold"
                  :class="user.enabled ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
                >
                  {{ user.enabled ? 'Active' : 'Disabled' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="role in user.krcs_roles"
                    :key="role"
                    class="px-2 py-1 bg-red-light text-red-dark rounded text-xs font-medium"
                  >
                    {{ role }}
                  </span>
                  <span v-if="user.krcs_roles.length === 0" class="text-xs text-medium-gray">No roles</span>
                </div>
              </td>
              <td class="px-4 py-3 text-right">
                <button
                  @click="openEditModal(user)"
                  class="text-sm text-red-primary hover:text-red-dark font-medium mr-3"
                >
                  Edit
                </button>
                <button
                  @click="handleToggleUser(user)"
                  class="text-sm hover:underline"
                  :class="user.enabled ? 'text-medium-gray' : 'text-green-600'"
                >
                  {{ user.enabled ? 'Disable' : 'Enable' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="users.length === 0" class="text-center py-12 text-medium-gray">
        No users found
      </div>
    </div>

    <!-- Create User Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="closeCreateModal">
      <div class="bg-white rounded-lg shadow-elegant-xl max-w-lg w-full p-6">
        <h3 class="text-lg font-bold text-charcoal mb-4">Create New User</h3>

        <div class="space-y-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Email *</label>
            <input v-model="createForm.email" type="email" class="input w-full" placeholder="user@redcross.or.ke" />
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">First Name *</label>
            <input v-model="createForm.firstName" type="text" class="input w-full" />
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Last Name</label>
            <input v-model="createForm.lastName" type="text" class="input w-full" />
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Department</label>
            <select v-model="createForm.department" class="input w-full">
              <option value="">Select Department</option>
              <option v-for="dept in departments" :key="dept.name" :value="dept.name">
                {{ dept.department_name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Assign KRCS Roles</label>
            <div class="grid grid-cols-2 gap-2">
              <label v-for="role in krcsRoles" :key="role" class="flex items-center space-x-2 text-sm">
                <input type="checkbox" :value="role" v-model="createForm.roles" class="rounded" />
                <span>{{ role }}</span>
              </label>
            </div>
          </div>
        </div>

        <div v-if="error" class="text-sm text-red-600 mb-3">{{ error }}</div>

        <div class="flex space-x-3">
          <button @click="closeCreateModal" class="btn btn-outline flex-1">Cancel</button>
          <button
            @click="handleCreateUser"
            :disabled="actionLoading || !createForm.email || !createForm.firstName"
            class="btn btn-primary flex-1"
          >
            {{ actionLoading ? 'Creating...' : 'Create User' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="closeEditModal">
      <div class="bg-white rounded-lg shadow-elegant-xl max-w-lg w-full p-6">
        <h3 class="text-lg font-bold text-charcoal mb-1">Edit User</h3>
        <p class="text-sm text-medium-gray mb-4">{{ editingUser?.full_name || editingUser?.email }}</p>

        <div class="space-y-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Department</label>
            <select v-model="editForm.department" class="input w-full">
              <option value="">Select Department</option>
              <option v-for="dept in departments" :key="dept.name" :value="dept.name">
                {{ dept.department_name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Assign KRCS Roles</label>
            <div class="grid grid-cols-2 gap-2">
              <label v-for="role in krcsRoles" :key="role" class="flex items-center space-x-2 text-sm">
                <input type="checkbox" :value="role" v-model="editForm.roles" class="rounded" />
                <span>{{ role }}</span>
              </label>
            </div>
          </div>
        </div>

        <div v-if="error" class="text-sm text-red-600 mb-3">{{ error }}</div>

        <div class="flex space-x-3">
          <button @click="closeEditModal" class="btn btn-outline flex-1">Cancel</button>
          <button @click="handleUpdateUser" :disabled="actionLoading" class="btn btn-primary flex-1">
            {{ actionLoading ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../../composables/useApi'

const api = useApi()

const users = ref([])
const krcsRoles = ref([])
const departments = ref([])
const loading = ref(false)
const actionLoading = ref(false)
const error = ref('')

const showCreateModal = ref(false)
const createForm = ref({ email: '', firstName: '', lastName: '', department: '', roles: [] })

const showEditModal = ref(false)
const editingUser = ref(null)
const editForm = ref({ department: '', roles: [] })

const loadUsers = async () => {
  loading.value = true
  users.value = await api.getUsers()
  loading.value = false
}

const loadMeta = async () => {
  const meta = await api.getAdminMeta()
  krcsRoles.value = meta.krcs_roles || []
  departments.value = meta.departments || []
}

const closeCreateModal = () => {
  showCreateModal.value = false
  createForm.value = { email: '', firstName: '', lastName: '', department: '', roles: [] }
  error.value = ''
}

const handleCreateUser = async () => {
  if (!createForm.value.email || !createForm.value.firstName) return
  actionLoading.value = true
  error.value = ''
  const result = await api.createUser(
    createForm.value.email,
    createForm.value.firstName,
    createForm.value.lastName,
    createForm.value.department,
    createForm.value.roles
  )
  actionLoading.value = false
  if (result.success) {
    closeCreateModal()
    await loadUsers()
  } else {
    error.value = result.message || 'Failed to create user'
  }
}

const openEditModal = (user) => {
  editingUser.value = user
  editForm.value.department = user.krcs_department || ''
  editForm.value.roles = [...user.krcs_roles]
  showEditModal.value = true
  error.value = ''
}

const closeEditModal = () => {
  showEditModal.value = false
  editingUser.value = null
  editForm.value = { department: '', roles: [] }
  error.value = ''
}

const handleUpdateUser = async () => {
  if (!editingUser.value) return
  actionLoading.value = true
  error.value = ''
  const result = await api.updateUser(
    editingUser.value.name,
    editForm.value.department,
    editForm.value.roles
  )
  actionLoading.value = false
  if (result.success) {
    closeEditModal()
    await loadUsers()
  } else {
    error.value = result.message || 'Failed to update user'
  }
}

const handleToggleUser = async (user) => {
  const action = user.enabled ? 'disable' : 'enable'
  if (!confirm(`${action.charAt(0).toUpperCase() + action.slice(1)} user "${user.full_name || user.email}"?`)) return
  actionLoading.value = true
  error.value = ''
  const result = await api.toggleUserEnabled(user.name, !user.enabled)
  actionLoading.value = false
  if (result.success) {
    await loadUsers()
  } else {
    error.value = result.message || `Failed to ${action} user`
  }
}

onMounted(async () => {
  await Promise.all([loadUsers(), loadMeta()])
})
</script>
