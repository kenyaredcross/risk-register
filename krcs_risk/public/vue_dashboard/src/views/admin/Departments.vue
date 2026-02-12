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

    <!-- Add Department Form -->
    <div class="card mb-6">
      <h2 class="card-header">Add New Department</h2>
      <div class="flex gap-3">
        <input
          v-model="newDeptName"
          type="text"
          placeholder="Department Name"
          class="input flex-1"
          @keyup.enter="handleCreateDepartment"
        />
        <button @click="handleCreateDepartment" :disabled="!newDeptName.trim() || loading" class="btn btn-primary">
          {{ loading ? 'Creating...' : 'Add Department' }}
        </button>
      </div>
      <div v-if="error" class="text-sm text-red-600 mt-2">{{ error }}</div>
    </div>

    <!-- Departments List -->
    <div v-if="loadingList" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-primary"></div>
    </div>

    <div v-else class="space-y-4">
      <div v-for="dept in departments" :key="dept.name" class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-charcoal">{{ dept.department_name }}</h3>
          <button
            @click="confirmDeleteDepartment(dept)"
            class="text-sm text-red-primary hover:text-red-dark font-medium"
            title="Delete Department"
          >
            Delete
          </button>
        </div>

        <!-- Units List -->
        <div v-if="dept.units && dept.units.length > 0" class="space-y-2 mb-3">
          <div
            v-for="unit in dept.units"
            :key="unit.name"
            class="flex items-center justify-between bg-light-gray rounded p-3"
          >
            <span class="text-charcoal">{{ unit.unit_name }}</span>
            <button
              @click="confirmDeleteUnit(unit)"
              class="text-xs text-red-primary hover:text-red-dark font-medium"
            >
              Delete
            </button>
          </div>
        </div>
        <div v-else class="text-sm text-medium-gray mb-3">No units yet</div>

        <!-- Add Unit Form -->
        <div class="flex gap-2 border-t border-light-border pt-3">
          <input
            v-model="newUnitNames[dept.name]"
            type="text"
            placeholder="New Unit Name"
            class="input flex-1 text-sm"
            @keyup.enter="handleCreateUnit(dept)"
          />
          <button
            @click="handleCreateUnit(dept)"
            :disabled="!newUnitNames[dept.name]?.trim() || loading"
            class="btn btn-outline text-sm"
          >
            Add Unit
          </button>
        </div>
      </div>

      <div v-if="departments.length === 0" class="card text-center py-12">
        <p class="text-medium-gray">No departments yet. Add one above to get started.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../../composables/useApi'

const api = useApi()

const departments = ref([])
const newDeptName = ref('')
const newUnitNames = ref({})
const loading = ref(false)
const loadingList = ref(false)
const error = ref('')

const loadDepartments = async () => {
  loadingList.value = true
  departments.value = await api.getDepartments()
  loadingList.value = false
}

const handleCreateDepartment = async () => {
  if (!newDeptName.value.trim()) return
  loading.value = true
  error.value = ''
  const result = await api.createDepartment(newDeptName.value)
  loading.value = false
  if (result.success) {
    newDeptName.value = ''
    await loadDepartments()
  } else {
    error.value = result.message || 'Failed to create department'
  }
}

const handleCreateUnit = async (dept) => {
  const unitName = newUnitNames.value[dept.name]
  if (!unitName?.trim()) return
  loading.value = true
  error.value = ''
  const result = await api.createUnit(unitName, dept.name)
  loading.value = false
  if (result.success) {
    newUnitNames.value[dept.name] = ''
    await loadDepartments()
  } else {
    error.value = result.message || 'Failed to create unit'
  }
}

const confirmDeleteDepartment = (dept) => {
  if (confirm(`Delete department "${dept.department_name}"? This will fail if risks or units are linked.`)) {
    deleteDepartment(dept)
  }
}

const deleteDepartment = async (dept) => {
  loading.value = true
  error.value = ''
  const result = await api.deleteDepartment(dept.name)
  loading.value = false
  if (result.success) {
    await loadDepartments()
  } else {
    error.value = result.message || 'Failed to delete department'
  }
}

const confirmDeleteUnit = (unit) => {
  if (confirm(`Delete unit "${unit.unit_name}"?`)) {
    deleteUnit(unit)
  }
}

const deleteUnit = async (unit) => {
  loading.value = true
  error.value = ''
  const result = await api.deleteUnit(unit.name)
  loading.value = false
  if (result.success) {
    await loadDepartments()
  } else {
    error.value = result.message || 'Failed to delete unit'
  }
}

onMounted(() => {
  loadDepartments()
})
</script>
