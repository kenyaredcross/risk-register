<template>
  <div class="animate-fade-in">
    <div class="mb-6">
      <button @click="router.back()" class="text-medium-gray hover:text-charcoal mb-4 flex items-center space-x-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        <span>Back</span>
      </button>
      <h1 class="text-3xl font-bold text-charcoal mb-2">Create New Risk</h1>
      <p class="text-medium-gray">Submit a new risk to the register</p>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Basic Information -->
      <div class="card">
        <h2 class="card-header">Basic Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="relative">
            <label class="block text-sm font-medium text-charcoal mb-1">Project</label>
            <input
              v-model="projectSearch"
              @focus="projectDropdownOpen = true"
              @blur="closeProjectDropdown"
              type="text"
              class="input w-full"
              placeholder="Search or select project..."
            />
            <div
              v-if="projectDropdownOpen"
              class="absolute z-10 mt-1 w-full bg-white border border-light-border rounded-lg shadow-lg max-h-60 overflow-auto"
            >
              <button
                type="button"
                @mousedown.prevent="openCreateProjectModal"
                class="w-full text-left px-4 py-2 text-sm hover:bg-light-gray flex items-center space-x-2 text-red-primary font-medium border-b border-light-border"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <span>Create New Project</span>
              </button>
              <button
                v-for="proj in filteredProjects"
                :key="proj.name"
                type="button"
                @mousedown.prevent="selectProject(proj)"
                class="w-full text-left px-4 py-2 text-sm hover:bg-light-gray"
              >
                {{ proj.project_name }}
              </button>
              <div v-if="filteredProjects.length === 0" class="px-4 py-3 text-sm text-medium-gray text-center">
                No projects found
              </div>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Department *</label>
            <select v-model="form.department" required class="input w-full bg-light-gray" disabled>
              <option value="">Select Department</option>
              <option v-for="dept in departments" :key="dept.name" :value="dept.name">{{ dept.department_name }}</option>
            </select>
            <p v-if="currentUser && currentUser.department" class="text-xs text-medium-gray mt-1">
              Auto-populated from your user profile
            </p>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Unit</label>
            <select v-model="form.unit" class="input w-full" :disabled="!form.department">
              <option value="">Select Unit</option>
              <option v-for="unit in filteredUnits" :key="unit.name" :value="unit.name">{{ unit.unit_name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Region</label>
            <select v-model="form.region" class="input w-full">
              <option value="">Select Region</option>
              <option v-for="region in regions" :key="region.name" :value="region.name">{{ region.region_name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Risk Category *</label>
            <select v-model="form.risk_category" required class="input w-full">
              <option value="">Select Category</option>
              <option value="Financial">Financial</option>
              <option value="Operational">Operational</option>
              <option value="Strategic">Strategic</option>
              <option value="Compliance">Compliance</option>
              <option value="Reputational">Reputational</option>
              <option value="Technology">Technology</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Risk Owner</label>
            <select v-model="form.risk_owner" class="input w-full">
              <option value="">Select Risk Owner</option>
              <option v-for="user in krcsUsers" :key="user.name" :value="user.name">
                {{ user.full_name }} ({{ user.roles_display }})
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Risk Description -->
      <div class="card">
        <h2 class="card-header">Risk Description</h2>
        <div>
          <label class="block text-sm font-medium text-charcoal mb-1">Risk Description *</label>
          <textarea v-model="form.risk_description" required rows="4" class="input w-full" placeholder="Describe the risk..."></textarea>
        </div>
      </div>

      <!-- Possible Causes -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-charcoal">Possible Causes</h2>
          <button type="button" @click="addCause" class="btn btn-outline btn-sm">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Cause
          </button>
        </div>
        <div v-if="form.possible_causes.length === 0" class="text-sm text-medium-gray text-center py-4">
          No causes added yet. Click "Add Cause" to add one.
        </div>
        <div v-else class="space-y-3">
          <div v-for="(cause, index) in form.possible_causes" :key="index" class="flex gap-2">
            <textarea
              v-model="cause.cause_description"
              rows="2"
              class="input w-full"
              placeholder="Describe a possible cause..."
            ></textarea>
            <button type="button" @click="removeCause(index)" class="text-red-primary hover:text-red-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Effects / Consequences -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-charcoal">Effects / Consequences</h2>
          <button type="button" @click="addEffect" class="btn btn-outline btn-sm">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Effect
          </button>
        </div>
        <div v-if="form.effects.length === 0" class="text-sm text-medium-gray text-center py-4">
          No effects added yet. Click "Add Effect" to add one.
        </div>
        <div v-else class="space-y-3">
          <div v-for="(effect, index) in form.effects" :key="index" class="flex gap-2">
            <textarea
              v-model="effect.consequence_description"
              rows="2"
              class="input w-full"
              placeholder="Describe a possible effect/consequence..."
            ></textarea>
            <button type="button" @click="removeEffect(index)" class="text-red-primary hover:text-red-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mitigating Actions -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-charcoal">Mitigating Actions</h2>
          <button type="button" @click="addAction" class="btn btn-outline btn-sm">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Action
          </button>
        </div>
        <div v-if="form.mitigating_actions.length === 0" class="text-sm text-medium-gray text-center py-4">
          No mitigating actions added yet. Click "Add Action" to add one.
        </div>
        <div v-else class="space-y-4">
          <div v-for="(action, index) in form.mitigating_actions" :key="index" class="border border-light-border rounded-lg p-4 relative">
            <button type="button" @click="removeAction(index)" class="absolute top-2 right-2 text-red-primary hover:text-red-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-charcoal mb-1">Action Description *</label>
                <textarea
                  v-model="action.action_description"
                  rows="2"
                  class="input w-full"
                  placeholder="Describe the mitigating action..."
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-charcoal mb-1">Responsible Person</label>
                <input
                  v-model="action.responsible_person"
                  type="text"
                  class="input w-full"
                  placeholder="Person responsible"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-charcoal mb-1">Deadline</label>
                <input
                  v-model="action.deadline"
                  type="date"
                  class="input w-full"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Risk Assessment -->
      <div class="card">
        <h2 class="card-header">Risk Assessment</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Likelihood (1-5) *</label>
            <div class="flex items-center space-x-3">
              <input v-model.number="form.likelihood" type="range" min="1" max="5" required class="flex-1" />
              <span class="text-2xl font-bold text-charcoal w-8 text-center">{{ form.likelihood }}</span>
            </div>
            <div class="text-xs text-medium-gray mt-1">1 = Very Unlikely, 5 = Very Likely</div>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Impact (1-5) *</label>
            <div class="flex items-center space-x-3">
              <input v-model.number="form.impact" type="range" min="1" max="5" required class="flex-1" />
              <span class="text-2xl font-bold text-charcoal w-8 text-center">{{ form.impact }}</span>
            </div>
            <div class="text-xs text-medium-gray mt-1">1 = Negligible, 5 = Catastrophic</div>
          </div>
          <div class="md:col-span-2 bg-light-gray rounded-lg p-4">
            <div class="text-sm text-medium-gray mb-1">Overall Rating (Auto-calculated)</div>
            <div class="text-3xl font-bold" :class="getRatingColor(overallRating)">
              {{ overallRating }} — {{ riskLevel }}
            </div>
          </div>
        </div>
      </div>

      <!-- Review Schedule -->
      <div class="card">
        <h2 class="card-header">Review Schedule</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Review Frequency</label>
            <select v-model="form.review_frequency" class="input w-full">
              <option value="">Not Scheduled</option>
              <option value="Daily">Daily</option>
              <option value="Weekly">Weekly</option>
              <option value="Fortnightly">Fortnightly</option>
              <option value="Monthly">Monthly</option>
              <option value="Quarterly">Quarterly</option>
              <option value="Semi-Annual">Semi-Annual</option>
              <option value="Annual">Annual</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Timeline</label>
            <input v-model="form.timeline" type="text" class="input w-full" placeholder="e.g., Q1 2026" />
          </div>
        </div>
      </div>

      <!-- Additional Information -->
      <div class="card">
        <h2 class="card-header">Additional Information</h2>
        <div>
          <label class="block text-sm font-medium text-charcoal mb-1">Remarks</label>
          <textarea v-model="form.remarks" rows="2" class="input w-full" placeholder="Any additional notes..."></textarea>
        </div>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="card bg-red-50 border border-red-200">
        <p class="text-sm text-red-700">{{ error }}</p>
      </div>

      <!-- Actions -->
      <div class="flex justify-end space-x-3">
        <button type="button" @click="router.back()" class="btn btn-outline">Cancel</button>
        <button type="submit" :disabled="loading" class="btn btn-primary">
          {{ loading ? 'Creating...' : 'Create Risk' }}
        </button>
      </div>
    </form>

    <!-- Create Project Modal -->
    <div v-if="createProjectModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="closeCreateProjectModal">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4" @click.stop>
        <div class="px-6 py-4 border-b border-light-border">
          <h3 class="text-xl font-bold text-charcoal">Create New Project</h3>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Project Name *</label>
            <input
              v-model="newProjectName"
              type="text"
              class="input w-full"
              placeholder="Enter project name"
              @keydown.enter="handleCreateProject"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Project Code (ID) *</label>
            <input
              v-model="newProjectCode"
              type="text"
              class="input w-full"
              placeholder="Unique project code/ID"
              @keydown.enter="handleCreateProject"
            />
            <p class="text-xs text-medium-gray mt-1">Must be unique identifier for this project</p>
          </div>
          <div v-if="createProjectError" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <p class="text-sm text-red-700">{{ createProjectError }}</p>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-light-border flex justify-end space-x-3">
          <button type="button" @click="closeCreateProjectModal" class="btn btn-outline">Cancel</button>
          <button type="button" @click="handleCreateProject" :disabled="creatingProject" class="btn btn-primary">
            {{ creatingProject ? 'Creating...' : 'Create Project' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useApi } from '../composables/useApi'

const router = useRouter()
const api = useApi()

const loading = ref(false)
const error = ref('')

const departments = ref([])
const projects = ref([])
const regions = ref([])
const allUnits = ref([])
const krcsUsers = ref([])
const currentUser = ref(null)

// Project searchable dropdown state
const projectSearch = ref('')
const projectDropdownOpen = ref(false)
const selectedProjectName = ref('')

// Create project modal state
const createProjectModalOpen = ref(false)
const newProjectName = ref('')
const newProjectCode = ref('')
const creatingProject = ref(false)
const createProjectError = ref('')

const form = ref({
  project: '',
  department: '',
  unit: '',
  region: '',
  risk_category: '',
  risk_owner: '',
  risk_description: '',
  possible_causes: [],
  effects: [],
  mitigating_actions: [],
  likelihood: 3,
  impact: 3,
  review_frequency: '',
  timeline: '',
  remarks: ''
})

const overallRating = computed(() => form.value.likelihood * form.value.impact)

const riskLevel = computed(() => {
  const rating = overallRating.value
  if (rating >= 15) return 'Critical'
  if (rating >= 10) return 'High'
  if (rating >= 5) return 'Medium'
  return 'Low'
})

const filteredUnits = computed(() => {
  if (!form.value.department) return []
  return allUnits.value.filter(u => u.department === form.value.department)
})

const filteredProjects = computed(() => {
  if (!projectSearch.value.trim()) return projects.value
  const search = projectSearch.value.toLowerCase()
  return projects.value.filter(p =>
    p.project_name.toLowerCase().includes(search) ||
    p.name.toLowerCase().includes(search)
  )
})

const getRatingColor = (rating) => {
  if (rating >= 15) return 'text-red-primary'
  if (rating >= 10) return 'text-orange-600'
  if (rating >= 5) return 'text-yellow-600'
  return 'text-green-600'
}

const addCause = () => {
  form.value.possible_causes.push({ cause_description: '' })
}

const removeCause = (index) => {
  form.value.possible_causes.splice(index, 1)
}

const addEffect = () => {
  form.value.effects.push({ consequence_description: '' })
}

const removeEffect = (index) => {
  form.value.effects.splice(index, 1)
}

const addAction = () => {
  form.value.mitigating_actions.push({
    action_description: '',
    responsible_person: '',
    deadline: '',
    status: 'Pending'
  })
}

const removeAction = (index) => {
  form.value.mitigating_actions.splice(index, 1)
}

const selectProject = (proj) => {
  form.value.project = proj.name
  selectedProjectName.value = proj.project_name
  projectSearch.value = proj.project_name
  projectDropdownOpen.value = false
}

const closeProjectDropdown = () => {
  setTimeout(() => {
    projectDropdownOpen.value = false
  }, 200)
}

const openCreateProjectModal = () => {
  projectDropdownOpen.value = false
  createProjectModalOpen.value = true
  newProjectName.value = ''
  newProjectCode.value = ''
  createProjectError.value = ''
}

const closeCreateProjectModal = () => {
  createProjectModalOpen.value = false
  newProjectName.value = ''
  newProjectCode.value = ''
  createProjectError.value = ''
}

const handleCreateProject = async () => {
  if (!newProjectName.value.trim()) {
    createProjectError.value = 'Project name is required'
    return
  }

  if (!newProjectCode.value.trim()) {
    createProjectError.value = 'Project code is required'
    return
  }

  creatingProject.value = true
  createProjectError.value = ''

  try {
    const projectData = {
      doctype: 'Project',
      project_name: newProjectName.value.trim(),
      project_code: newProjectCode.value.trim()
    }

    const res = await axios.post('/api/resource/Project', projectData)

    if (res.data && res.data.data) {
      // Add to local projects list
      const newProj = {
        name: res.data.data.name,
        project_name: res.data.data.project_name
      }
      projects.value.push(newProj)

      // Select the newly created project
      selectProject(newProj)
      closeCreateProjectModal()
    } else {
      createProjectError.value = 'Failed to create project. Please try again.'
    }
  } catch (err) {
    const errorMsg = err.response?.data?.message || err.response?.data?.exc || 'An error occurred while creating the project.'
    // Check for duplicate error
    if (errorMsg.includes('Duplicate') || errorMsg.includes('already exists')) {
      createProjectError.value = 'A project with this code already exists. Please use a unique project code.'
    } else {
      createProjectError.value = errorMsg
    }
    console.error('Error creating project:', err)
  } finally {
    creatingProject.value = false
  }
}

const loadMasterData = async () => {
  try {
    // Fetch current user and auto-populate department
    const user = await api.getCurrentUser()
    currentUser.value = user
    if (user && user.department) {
      form.value.department = user.department
    }

    // Fetch departments with units
    const deptRes = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_departments')
    const depts = deptRes.data.message || []
    departments.value = depts
    allUnits.value = depts.flatMap(d => d.units || [])

    // Fetch projects
    const projRes = await axios.get('/api/resource/Project', {
      params: { fields: JSON.stringify(['name', 'project_name']), limit_page_length: 999 }
    })
    projects.value = projRes.data.data || []

    // Fetch regions
    const regRes = await axios.get('/api/resource/Region', {
      params: { fields: JSON.stringify(['name', 'region_name']), limit_page_length: 999 }
    })
    regions.value = regRes.data.data || []

    // Fetch users with KRCS roles
    const usersRes = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_users')
    krcsUsers.value = usersRes.data.message || []
  } catch (err) {
    console.error('Failed to load master data', err)
  }
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    // Format child tables with proper doctype field
    const possibleCauses = form.value.possible_causes
      .filter(c => c.cause_description && c.cause_description.trim())
      .map(c => ({
        doctype: 'Possible Cause',
        cause_description: c.cause_description.trim()
      }))

    const effects = form.value.effects
      .filter(e => e.consequence_description && e.consequence_description.trim())
      .map(e => ({
        doctype: 'Risk Consequence',
        consequence_description: e.consequence_description.trim()
      }))

    const mitigatingActions = form.value.mitigating_actions
      .filter(a => a.action_description && a.action_description.trim())
      .map(a => ({
        doctype: 'Mitigating Action',
        action_description: a.action_description.trim(),
        responsible_person: a.responsible_person || null,
        deadline: a.deadline || null,
        status: 'Pending'
      }))

    const docData = {
      doctype: 'Program Risk Register',
      project: form.value.project || null,
      department: form.value.department,
      unit: form.value.unit || null,
      region: form.value.region || null,
      risk_category: form.value.risk_category,
      risk_owner: form.value.risk_owner || null,
      risk_description: form.value.risk_description,
      // Child table fields with proper doctype
      possible_causes: possibleCauses,
      effects: effects,
      mitigating_actions: mitigatingActions,
      likelihood: form.value.likelihood,
      impact: form.value.impact,
      review_frequency: form.value.review_frequency || null,
      timeline: form.value.timeline || null,
      remarks: form.value.remarks || null,
      status: 'Draft'
    }

    const res = await axios.post('/api/resource/Program Risk Register', docData)

    if (res.data && res.data.data) {
      // Success - redirect to the new risk detail page
      router.push(`/risk/${res.data.data.name}`)
    } else {
      error.value = 'Failed to create risk. Please try again.'
    }
  } catch (err) {
    error.value = err.response?.data?.message || err.response?.data?.exc || 'An error occurred while creating the risk.'
    console.error('Error creating risk:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMasterData()
})
</script>
