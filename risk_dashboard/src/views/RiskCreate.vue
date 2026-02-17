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

    <!-- Step Indicator -->
    <div class="flex items-center mb-8">
      <template v-for="(s, i) in steps" :key="i">
        <div class="flex items-center">
          <div
            class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-colors"
            :class="currentStep > i + 1
              ? 'bg-green-500 text-white'
              : currentStep === i + 1
                ? 'bg-red-primary text-white'
                : 'bg-light-gray text-medium-gray'"
          >
            <svg v-if="currentStep > i + 1" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
            </svg>
            <span v-else>{{ i + 1 }}</span>
          </div>
          <span
            class="ml-2 text-sm font-medium hidden sm:block"
            :class="currentStep === i + 1 ? 'text-charcoal' : 'text-medium-gray'"
          >{{ s }}</span>
        </div>
        <div v-if="i < steps.length - 1" class="flex-1 h-px mx-3" :class="currentStep > i + 1 ? 'bg-green-500' : 'bg-light-border'" />
      </template>
    </div>

    <!-- ── Step 1: Basic Information ── -->
    <div v-if="currentStep === 1" class="space-y-6">
      <div class="card">
        <h2 class="card-header">Basic Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

          <!-- Risk Type — first field, drives visibility of other fields -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-charcoal mb-1">Risk Type *</label>
            <select v-model="form.risk_type" class="input w-full md:w-1/2">
              <option value="">Select Risk Type</option>
              <option v-if="isGlobalViewer" value="Corporate">Corporate</option>
              <option value="Departmental">Departmental</option>
              <option value="Project">Project</option>
            </select>
          </div>

          <!-- Project (only shown when Risk Type = Project) -->
          <div v-if="form.risk_type === 'Project'" class="relative">
            <label class="block text-sm font-medium text-charcoal mb-1">Project</label>
            <input
              v-model="projectSearch"
              @focus="projectDropdownOpen = true"
              @blur="closeProjectDropdown"
              type="text"
              class="input w-full"
              placeholder="Search or select project..."
            />
            <div v-if="projectDropdownOpen" class="absolute z-10 mt-1 w-full bg-white border border-light-border rounded-lg shadow-lg max-h-60 overflow-auto">
              <button type="button" @mousedown.prevent="openCreateProjectModal"
                class="w-full text-left px-4 py-2 text-sm hover:bg-light-gray flex items-center space-x-2 text-red-primary font-medium border-b border-light-border">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                <span>Create New Project</span>
              </button>
              <button v-for="proj in filteredProjects" :key="proj.name" type="button"
                @mousedown.prevent="selectProject(proj)" class="w-full text-left px-4 py-2 text-sm hover:bg-light-gray">
                {{ proj.project_name }}
              </button>
              <div v-if="filteredProjects.length === 0" class="px-4 py-3 text-sm text-medium-gray text-center">No projects found</div>
            </div>
          </div>

          <!-- Department (hidden for Corporate risks) -->
          <div v-if="form.risk_type !== 'Corporate'" class="relative">
            <label class="block text-sm font-medium text-charcoal mb-1">Department *</label>
            <input type="hidden" :value="form.department" />
            <input
              v-model="departmentSearch"
              @focus="departmentDropdownOpen = true"
              @blur="closeDepartmentDropdown"
              type="text"
              class="input w-full"
              placeholder="Search or select department..."
            />
            <div v-if="departmentDropdownOpen" class="absolute z-10 mt-1 w-full bg-white border border-light-border rounded-lg shadow-lg max-h-60 overflow-auto">
              <button type="button" @mousedown.prevent="openCreateDepartmentModal"
                class="w-full text-left px-4 py-2 text-sm hover:bg-light-gray flex items-center space-x-2 text-red-primary font-medium border-b border-light-border">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                <span>Create New Department</span>
              </button>
              <button v-for="dept in filteredDepartments" :key="dept.name" type="button"
                @mousedown.prevent="selectDepartment(dept)" class="w-full text-left px-4 py-2 text-sm hover:bg-light-gray">
                {{ dept.department_name }}
              </button>
              <div v-if="filteredDepartments.length === 0" class="px-4 py-3 text-sm text-medium-gray text-center">No departments found</div>
            </div>
          </div>

          <!-- Unit (hidden for Corporate risks) -->
          <div v-if="form.risk_type !== 'Corporate'" class="relative">
            <label class="block text-sm font-medium text-charcoal mb-1">Unit</label>
            <input
              v-model="unitSearch"
              @focus="unitDropdownOpen = true"
              @blur="closeUnitDropdown"
              type="text"
              class="input w-full"
              :placeholder="form.department ? 'Search or select unit...' : 'Select a department first'"
              :disabled="!form.department"
            />
            <div v-if="unitDropdownOpen && form.department" class="absolute z-10 mt-1 w-full bg-white border border-light-border rounded-lg shadow-lg max-h-60 overflow-auto">
              <button type="button" @mousedown.prevent="openCreateUnitModal"
                class="w-full text-left px-4 py-2 text-sm hover:bg-light-gray flex items-center space-x-2 text-red-primary font-medium border-b border-light-border">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                <span>Create New Unit</span>
              </button>
              <button v-for="unit in filteredUnits" :key="unit.name" type="button"
                @mousedown.prevent="selectUnit(unit)" class="w-full text-left px-4 py-2 text-sm hover:bg-light-gray">
                {{ unit.unit_name }}
              </button>
              <div v-if="filteredUnits.length === 0" class="px-4 py-3 text-sm text-medium-gray text-center">No units found</div>
            </div>
          </div>

          <!-- Region -->
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Region</label>
            <select v-model="form.region" class="input w-full">
              <option value="">Select Region</option>
              <option v-for="region in regions" :key="region.name" :value="region.name">{{ region.region_name }}</option>
            </select>
          </div>

          <!-- Risk Category -->
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Risk Category *</label>
            <select v-model="form.risk_category" class="input w-full">
              <option value="">Select Category</option>
              <option value="Strategic">Strategic</option>
              <option value="Operational">Operational</option>
              <option value="Financial">Financial</option>
              <option value="Compliance">Compliance</option>
              <option value="Safeguarding & Security">Safeguarding &amp; Security</option>
              <option value="Reputational">Reputational</option>
            </select>
          </div>

          <!-- Risk Owner -->
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Risk Owner</label>
            <select v-model="form.risk_owner" class="input w-full">
              <option value="">Select Risk Owner</option>
              <option value="KRCS HOR">KRCS HOR</option>
              <option value="KRCS DSG">KRCS DSG</option>
              <option value="KRCS HOD">KRCS HOD</option>
              <option value="KRCS Project Manager">KRCS Project Manager</option>
              <option value="KRCS RPC">KRCS RPC</option>
              <option value="KRCS Finance Officer">KRCS Finance Officer</option>
              <option value="KRCS Procurement Manager">KRCS Procurement Manager</option>
              <option value="KRCS Logistics Manager">KRCS Logistics Manager</option>
              <option value="KRCS HR Manager">KRCS HR Manager</option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="step1Error" class="card bg-red-50 border border-red-200">
        <p class="text-sm text-red-700">{{ step1Error }}</p>
      </div>

      <div class="flex justify-end">
        <button type="button" @click="nextStep" class="btn btn-primary">
          Next: Risk Details
          <svg class="w-4 h-4 ml-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- ── Step 2: Risk Details ── -->
    <div v-if="currentStep === 2" class="space-y-6">

      <!-- Risk Description -->
      <div class="card">
        <h2 class="card-header">Risk Description</h2>
        <div>
          <label class="block text-sm font-medium text-charcoal mb-1">Risk Description *</label>
          <textarea v-model="form.risk_description" rows="4" class="input w-full" placeholder="Describe the risk..."></textarea>
        </div>
      </div>

      <!-- Possible Causes -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-charcoal">Possible Causes</h2>
          <button type="button" @click="addCause" class="btn btn-outline btn-sm">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
            Add Cause
          </button>
        </div>
        <div v-if="form.possible_causes.length === 0" class="text-sm text-medium-gray text-center py-4">
          No causes added yet. Click "Add Cause" to add one.
        </div>
        <div v-else class="space-y-3">
          <div v-for="(cause, index) in form.possible_causes" :key="index" class="flex gap-2">
            <textarea v-model="cause.cause_description" rows="2" class="input w-full" placeholder="Describe a possible cause..."></textarea>
            <button type="button" @click="removeCause(index)" class="text-red-primary hover:text-red-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Effects -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-charcoal">Effects / Consequences</h2>
          <button type="button" @click="addEffect" class="btn btn-outline btn-sm">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
            Add Effect
          </button>
        </div>
        <div v-if="form.effects.length === 0" class="text-sm text-medium-gray text-center py-4">
          No effects added yet. Click "Add Effect" to add one.
        </div>
        <div v-else class="space-y-3">
          <div v-for="(effect, index) in form.effects" :key="index" class="flex gap-2">
            <textarea v-model="effect.consequence_description" rows="2" class="input w-full" placeholder="Describe a possible effect/consequence..."></textarea>
            <button type="button" @click="removeEffect(index)" class="text-red-primary hover:text-red-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-charcoal">Actions</h2>
          <button type="button" @click="addAction" class="btn btn-outline btn-sm">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
            Add Action
          </button>
        </div>
        <div v-if="form.mitigating_actions.length === 0" class="text-sm text-medium-gray text-center py-4">
          No actions added yet. Click "Add Action" to add one.
        </div>
        <div v-else class="space-y-4">
          <div v-for="(action, index) in form.mitigating_actions" :key="index" class="border border-light-border rounded-lg p-4 relative">
            <button type="button" @click="removeAction(index)" class="absolute top-2 right-2 text-red-primary hover:text-red-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Addresses Cause (shown only when there are causes) -->
              <div v-if="form.possible_causes.filter(c => c.cause_description).length > 0" class="md:col-span-2">
                <label class="block text-sm font-medium text-charcoal mb-1">Addresses Cause</label>
                <select v-model="action.addresses_cause" class="input w-full">
                  <option :value="null">— Not linked to a specific cause —</option>
                  <option
                    v-for="(cause, ci) in form.possible_causes.filter(c => c.cause_description)"
                    :key="ci"
                    :value="ci + 1"
                  >
                    Cause {{ ci + 1 }}: {{ cause.cause_description.length > 80 ? cause.cause_description.substring(0, 80) + '…' : cause.cause_description }}
                  </option>
                </select>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-charcoal mb-1">Action Description *</label>
                <textarea v-model="action.action_description" rows="2" class="input w-full" placeholder="Describe the action..."></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-charcoal mb-1">Responsible Person</label>
                <input v-model="action.responsible_person" type="text" class="input w-full" placeholder="Person responsible" />
              </div>
              <div>
                <label class="block text-sm font-medium text-charcoal mb-1">Deadline</label>
                <input v-model="action.deadline" type="date" class="input w-full" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="step2Error" class="card bg-red-50 border border-red-200">
        <p class="text-sm text-red-700">{{ step2Error }}</p>
      </div>

      <div class="flex justify-between">
        <button type="button" @click="prevStep" class="btn btn-outline">
          <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
        <button type="button" @click="nextStep" class="btn btn-primary">
          Next: Assessment
          <svg class="w-4 h-4 ml-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- ── Step 3: Assessment & Schedule ── -->
    <div v-if="currentStep === 3" class="space-y-6">

      <div class="card">
        <h2 class="card-header">Risk Assessment</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Likelihood (1-5) *</label>
            <div class="flex items-center space-x-3">
              <input v-model.number="form.likelihood" type="range" min="1" max="5" class="flex-1 slider-red" />
              <span class="text-2xl font-bold text-charcoal w-8 text-center">{{ form.likelihood }}</span>
            </div>
            <div class="text-xs text-medium-gray mt-1">1 = Very Unlikely, 5 = Very Likely</div>
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Impact (1-5) *</label>
            <div class="flex items-center space-x-3">
              <input v-model.number="form.impact" type="range" min="1" max="5" class="flex-1 slider-red" />
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

      <div class="card">
        <h2 class="card-header">Additional Information</h2>
        <div>
          <label class="block text-sm font-medium text-charcoal mb-1">Remarks</label>
          <textarea v-model="form.remarks" rows="2" class="input w-full" placeholder="Any additional notes..."></textarea>
        </div>
      </div>

      <div class="flex justify-between">
        <button type="button" @click="prevStep" class="btn btn-outline">
          <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
        <button type="button" @click="nextStep" class="btn btn-primary">
          Next: Review
          <svg class="w-4 h-4 ml-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- ── Step 4: Review & Submit ── -->
    <div v-if="currentStep === 4" class="space-y-6">

      <div class="card">
        <h2 class="card-header">Review Your Risk</h2>

        <!-- Basic Info summary -->
        <div class="mb-6">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-semibold text-medium-gray uppercase tracking-wide">Basic Information</h3>
            <button type="button" @click="currentStep = 1" class="text-xs text-red-primary hover:underline">Edit</button>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <div><div class="text-xs text-medium-gray">Risk Type</div><div class="font-medium text-charcoal">{{ form.risk_type || '—' }}</div></div>
            <div v-if="form.risk_type === 'Project'"><div class="text-xs text-medium-gray">Project</div><div class="font-medium text-charcoal">{{ projectSearch || '—' }}</div></div>
            <div v-if="form.risk_type !== 'Corporate'"><div class="text-xs text-medium-gray">Department</div><div class="font-medium text-charcoal">{{ departmentSearch || '—' }}</div></div>
            <div v-if="form.risk_type !== 'Corporate'"><div class="text-xs text-medium-gray">Unit</div><div class="font-medium text-charcoal">{{ unitSearch || '—' }}</div></div>
            <div><div class="text-xs text-medium-gray">Region</div><div class="font-medium text-charcoal">{{ form.region || '—' }}</div></div>
            <div><div class="text-xs text-medium-gray">Category</div><div class="font-medium text-charcoal">{{ form.risk_category || '—' }}</div></div>
            <div><div class="text-xs text-medium-gray">Risk Owner</div><div class="font-medium text-charcoal">{{ form.risk_owner || '—' }}</div></div>
          </div>
        </div>

        <div class="border-t border-light-border pt-4 mb-6">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-semibold text-medium-gray uppercase tracking-wide">Risk Details</h3>
            <button type="button" @click="currentStep = 2" class="text-xs text-red-primary hover:underline">Edit</button>
          </div>
          <div class="mb-3">
            <div class="text-xs text-medium-gray mb-1">Description</div>
            <div class="text-charcoal">{{ form.risk_description || '—' }}</div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <div class="text-xs text-medium-gray mb-1">Causes ({{ form.possible_causes.filter(c => c.cause_description).length }})</div>
              <ul class="text-sm text-charcoal space-y-1">
                <li v-for="(c, i) in form.possible_causes.filter(c => c.cause_description)" :key="i" class="truncate">• {{ c.cause_description }}</li>
                <li v-if="!form.possible_causes.filter(c => c.cause_description).length" class="text-medium-gray">None</li>
              </ul>
            </div>
            <div>
              <div class="text-xs text-medium-gray mb-1">Effects ({{ form.effects.filter(e => e.consequence_description).length }})</div>
              <ul class="text-sm text-charcoal space-y-1">
                <li v-for="(e, i) in form.effects.filter(e => e.consequence_description)" :key="i" class="truncate">• {{ e.consequence_description }}</li>
                <li v-if="!form.effects.filter(e => e.consequence_description).length" class="text-medium-gray">None</li>
              </ul>
            </div>
            <div>
              <div class="text-xs text-medium-gray mb-1">Actions ({{ form.mitigating_actions.filter(a => a.action_description).length }})</div>
              <ul class="text-sm text-charcoal space-y-1">
                <li v-for="(a, i) in form.mitigating_actions.filter(a => a.action_description)" :key="i" class="truncate">• {{ a.action_description }}</li>
                <li v-if="!form.mitigating_actions.filter(a => a.action_description).length" class="text-medium-gray">None</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="border-t border-light-border pt-4">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-semibold text-medium-gray uppercase tracking-wide">Assessment</h3>
            <button type="button" @click="currentStep = 3" class="text-xs text-red-primary hover:underline">Edit</button>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div><div class="text-xs text-medium-gray">Likelihood</div><div class="font-medium text-charcoal">{{ form.likelihood }} / 5</div></div>
            <div><div class="text-xs text-medium-gray">Impact</div><div class="font-medium text-charcoal">{{ form.impact }} / 5</div></div>
            <div>
              <div class="text-xs text-medium-gray">Overall Rating</div>
              <div class="font-bold" :class="getRatingColor(overallRating)">{{ overallRating }} — {{ riskLevel }}</div>
            </div>
            <div><div class="text-xs text-medium-gray">Review</div><div class="font-medium text-charcoal">{{ form.review_frequency || 'Not scheduled' }}</div></div>
          </div>
        </div>
      </div>

      <div v-if="error" class="card bg-red-50 border border-red-200">
        <p class="text-sm text-red-700">{{ error }}</p>
      </div>

      <div class="flex flex-col sm:flex-row justify-between gap-3">
        <button type="button" @click="prevStep" class="btn btn-outline">
          <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
        <div class="flex gap-3 sm:justify-end flex-wrap">
          <button type="button" @click="handleSubmit(false, false)" :disabled="loading" class="btn btn-outline">
            {{ loading && submitMode === 'draft' ? 'Saving...' : 'Save as Draft' }}
          </button>
          <button type="button" @click="handleSubmit(true, false)" :disabled="loading" class="btn btn-outline">
            {{ loading && submitMode === 'another' ? 'Creating...' : 'Save & Add Another' }}
          </button>
          <button type="button" @click="handleSubmit(true, true)" :disabled="loading" class="btn btn-outline">
            {{ loading && submitMode === 'approvalAnother' ? 'Submitting...' : 'Submit for Approval & Add Another' }}
          </button>
          <button type="button" @click="handleSubmit(false, true)" :disabled="loading" class="btn btn-primary">
            {{ loading && submitMode === 'approval' ? 'Submitting...' : 'Submit for Approval' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ── Modals ── -->

    <!-- Create Project Modal -->
    <div v-if="createProjectModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="closeCreateProjectModal">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4" @click.stop>
        <div class="px-6 py-4 border-b border-light-border">
          <h3 class="text-xl font-bold text-charcoal">Create New Project</h3>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Project Name *</label>
            <input v-model="newProjectName" type="text" class="input w-full" placeholder="Enter project name" @keydown.enter="handleCreateProject" />
          </div>
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Project Code (ID) *</label>
            <input v-model="newProjectCode" type="text" class="input w-full" placeholder="Unique project code/ID" @keydown.enter="handleCreateProject" />
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

    <!-- Create Department Modal -->
    <div v-if="createDepartmentModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="closeCreateDepartmentModal">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4" @click.stop>
        <div class="px-6 py-4 border-b border-light-border">
          <h3 class="text-xl font-bold text-charcoal">Create New Department</h3>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Department Name *</label>
            <input v-model="newDepartmentName" type="text" class="input w-full" placeholder="Enter department name" @keydown.enter="handleCreateDepartment" />
          </div>
          <div v-if="createDepartmentError" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <p class="text-sm text-red-700">{{ createDepartmentError }}</p>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-light-border flex justify-end space-x-3">
          <button type="button" @click="closeCreateDepartmentModal" class="btn btn-outline">Cancel</button>
          <button type="button" @click="handleCreateDepartment" :disabled="creatingDepartment" class="btn btn-primary">
            {{ creatingDepartment ? 'Creating...' : 'Create Department' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Create Unit Modal -->
    <div v-if="createUnitModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="closeCreateUnitModal">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4" @click.stop>
        <div class="px-6 py-4 border-b border-light-border">
          <h3 class="text-xl font-bold text-charcoal">Create New Unit</h3>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-1">Unit Name *</label>
            <input v-model="newUnitName" type="text" class="input w-full" placeholder="Enter unit name" @keydown.enter="handleCreateUnit" />
          </div>
          <div class="bg-light-gray rounded-lg px-4 py-2 text-sm text-medium-gray">
            Will be created under: <span class="font-medium text-charcoal">{{ selectedDepartmentName }}</span>
          </div>
          <div v-if="createUnitError" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <p class="text-sm text-red-700">{{ createUnitError }}</p>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-light-border flex justify-end space-x-3">
          <button type="button" @click="closeCreateUnitModal" class="btn btn-outline">Cancel</button>
          <button type="button" @click="handleCreateUnit" :disabled="creatingUnit" class="btn btn-primary">
            {{ creatingUnit ? 'Creating...' : 'Create Unit' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useApi } from '../composables/useApi'

const router = useRouter()
const api = useApi()

// ── Wizard state ──────────────────────────────────────────────────────────────
const steps = ['Basic Info', 'Risk Details', 'Assessment', 'Review & Submit']
const currentStep = ref(1)
const step1Error = ref('')
const step2Error = ref('')

// ── Master data ───────────────────────────────────────────────────────────────
const loading = ref(false)
const submitMode = ref('') // 'draft' | 'another' | 'approval'
const error = ref('')
const departments = ref([])
const projects = ref([])
const regions = ref([])
const allUnits = ref([])
const currentUser = ref(null)

// ── Project dropdown ──────────────────────────────────────────────────────────
const projectSearch = ref('')
const projectDropdownOpen = ref(false)
const selectedProjectName = ref('')
const createProjectModalOpen = ref(false)
const newProjectName = ref('')
const newProjectCode = ref('')
const creatingProject = ref(false)
const createProjectError = ref('')

// ── Department dropdown ───────────────────────────────────────────────────────
const departmentSearch = ref('')
const departmentDropdownOpen = ref(false)
const selectedDepartmentName = ref('')
const createDepartmentModalOpen = ref(false)
const newDepartmentName = ref('')
const creatingDepartment = ref(false)
const createDepartmentError = ref('')

// ── Unit dropdown ─────────────────────────────────────────────────────────────
const unitSearch = ref('')
const unitDropdownOpen = ref(false)
const createUnitModalOpen = ref(false)
const newUnitName = ref('')
const creatingUnit = ref(false)
const createUnitError = ref('')

// ── Form ──────────────────────────────────────────────────────────────────────
const form = ref({
  project: '',
  department: '',
  unit: '',
  region: '',
  risk_category: '',
  risk_type: '',
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

// ── Computed ──────────────────────────────────────────────────────────────────
const isGlobalViewer = computed(() => currentUser.value?.is_global_viewer === true)
const overallRating = computed(() => form.value.likelihood * form.value.impact)

const riskLevel = computed(() => {
  const r = overallRating.value
  if (r >= 15) return 'Critical'
  if (r >= 10) return 'High'
  if (r >= 5) return 'Medium'
  return 'Low'
})

const filteredProjects = computed(() => {
  if (!projectSearch.value.trim()) return projects.value
  const s = projectSearch.value.toLowerCase()
  return projects.value.filter(p => p.project_name.toLowerCase().includes(s) || p.name.toLowerCase().includes(s))
})

const filteredDepartments = computed(() => {
  if (!departmentSearch.value.trim()) return departments.value
  const s = departmentSearch.value.toLowerCase()
  return departments.value.filter(d => d.department_name.toLowerCase().includes(s))
})

const filteredUnits = computed(() => {
  const deptUnits = allUnits.value.filter(u => u.department === form.value.department)
  if (!unitSearch.value.trim()) return deptUnits
  const s = unitSearch.value.toLowerCase()
  return deptUnits.filter(u => u.unit_name.toLowerCase().includes(s))
})

// ── Helpers ───────────────────────────────────────────────────────────────────
const getRatingColor = (rating) => {
  if (rating >= 15) return 'text-red-primary'
  if (rating >= 10) return 'text-orange-600'
  if (rating >= 5) return 'text-yellow-600'
  return 'text-green-600'
}

// ── Step navigation ───────────────────────────────────────────────────────────
const nextStep = () => {
  if (currentStep.value === 1) {
    if (!form.value.risk_type) { step1Error.value = 'Risk Type is required.'; return }
    if (form.value.risk_type !== 'Corporate' && !form.value.department) { step1Error.value = 'Department is required.'; return }
    if (!form.value.risk_category) { step1Error.value = 'Risk Category is required.'; return }
    step1Error.value = ''
  }
  if (currentStep.value === 2) {
    if (!form.value.risk_description.trim()) { step2Error.value = 'Risk Description is required.'; return }
    step2Error.value = ''
  }
  currentStep.value++
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const prevStep = () => {
  currentStep.value--
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ── Child table helpers ───────────────────────────────────────────────────────
const addCause = () => form.value.possible_causes.push({ cause_description: '' })
const removeCause = (i) => form.value.possible_causes.splice(i, 1)
const addEffect = () => form.value.effects.push({ consequence_description: '' })
const removeEffect = (i) => form.value.effects.splice(i, 1)
const addAction = () => form.value.mitigating_actions.push({ action_description: '', responsible_person: '', deadline: '', status: 'Pending', addresses_cause: null })
const removeAction = (i) => form.value.mitigating_actions.splice(i, 1)

// Clear fields based on risk_type changes
watch(() => form.value.risk_type, (newType) => {
  if (newType !== 'Project') {
    form.value.project = ''
    projectSearch.value = ''
  }
  if (newType === 'Corporate') {
    form.value.department = ''
    form.value.unit = ''
    departmentSearch.value = ''
    unitSearch.value = ''
  }
})

// ── Project dropdown ──────────────────────────────────────────────────────────
const selectProject = (proj) => {
  form.value.project = proj.name
  selectedProjectName.value = proj.project_name
  projectSearch.value = proj.project_name
  projectDropdownOpen.value = false
}
const closeProjectDropdown = () => setTimeout(() => { projectDropdownOpen.value = false }, 200)
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
  if (!newProjectName.value.trim()) { createProjectError.value = 'Project name is required'; return }
  if (!newProjectCode.value.trim()) { createProjectError.value = 'Project code is required'; return }
  creatingProject.value = true
  createProjectError.value = ''
  try {
    const res = await axios.post('/api/resource/Project', {
      doctype: 'Project',
      project_name: newProjectName.value.trim(),
      project_code: newProjectCode.value.trim()
    })
    if (res.data?.data) {
      const newProj = { name: res.data.data.name, project_name: res.data.data.project_name }
      projects.value.push(newProj)
      selectProject(newProj)
      closeCreateProjectModal()
    } else {
      createProjectError.value = 'Failed to create project.'
    }
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data?.exc || 'An error occurred.'
    createProjectError.value = (msg.includes('Duplicate') || msg.includes('already exists'))
      ? 'A project with this code already exists.'
      : msg
  } finally {
    creatingProject.value = false
  }
}

// ── Department dropdown ───────────────────────────────────────────────────────
const selectDepartment = (dept) => {
  form.value.department = dept.name
  selectedDepartmentName.value = dept.department_name
  departmentSearch.value = dept.department_name
  departmentDropdownOpen.value = false
  form.value.unit = ''
  unitSearch.value = ''
}
const closeDepartmentDropdown = () => setTimeout(() => { departmentDropdownOpen.value = false }, 200)
const openCreateDepartmentModal = () => {
  departmentDropdownOpen.value = false
  createDepartmentModalOpen.value = true
  newDepartmentName.value = ''
  createDepartmentError.value = ''
}
const closeCreateDepartmentModal = () => {
  createDepartmentModalOpen.value = false
  newDepartmentName.value = ''
  createDepartmentError.value = ''
}
const handleCreateDepartment = async () => {
  if (!newDepartmentName.value.trim()) { createDepartmentError.value = 'Department name is required'; return }
  creatingDepartment.value = true
  createDepartmentError.value = ''
  try {
    const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.create_department', {
      department_name: newDepartmentName.value.trim()
    })
    const result = res.data.message || {}
    if (result.success) {
      const newDept = { name: result.name, department_name: newDepartmentName.value.trim(), units: [] }
      departments.value.push(newDept)
      selectDepartment(newDept)
      closeCreateDepartmentModal()
    } else {
      createDepartmentError.value = result.message || 'Failed to create department.'
    }
  } catch (err) {
    createDepartmentError.value = err.response?.data?.message || 'An error occurred.'
  } finally {
    creatingDepartment.value = false
  }
}

// ── Unit dropdown ─────────────────────────────────────────────────────────────
const selectUnit = (unit) => {
  form.value.unit = unit.name
  unitSearch.value = unit.unit_name
  unitDropdownOpen.value = false
}
const closeUnitDropdown = () => setTimeout(() => { unitDropdownOpen.value = false }, 200)
const openCreateUnitModal = () => {
  unitDropdownOpen.value = false
  createUnitModalOpen.value = true
  newUnitName.value = ''
  createUnitError.value = ''
}
const closeCreateUnitModal = () => {
  createUnitModalOpen.value = false
  newUnitName.value = ''
  createUnitError.value = ''
}
const handleCreateUnit = async () => {
  if (!newUnitName.value.trim()) { createUnitError.value = 'Unit name is required'; return }
  creatingUnit.value = true
  createUnitError.value = ''
  try {
    const res = await axios.post('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.create_unit', {
      unit_name: newUnitName.value.trim(),
      department: form.value.department
    })
    const result = res.data.message || {}
    if (result.success) {
      const newUnit = { name: result.name, unit_name: newUnitName.value.trim(), department: form.value.department }
      allUnits.value.push(newUnit)
      selectUnit(newUnit)
      closeCreateUnitModal()
    } else {
      createUnitError.value = result.message || 'Failed to create unit.'
    }
  } catch (err) {
    createUnitError.value = err.response?.data?.message || 'An error occurred.'
  } finally {
    creatingUnit.value = false
  }
}

// ── Submit ────────────────────────────────────────────────────────────────────
/**
 * @param {boolean} addAnother       — reset risk fields and stay on form to add another
 * @param {boolean} forApproval      — after saving, immediately submit for approval
 */
const handleSubmit = async (addAnother, forApproval = false) => {
  submitMode.value = addAnother && forApproval ? 'approvalAnother' : addAnother ? 'another' : forApproval ? 'approval' : 'draft'
  loading.value = true
  error.value = ''
  try {
    const possibleCauses = form.value.possible_causes
      .filter(c => c.cause_description?.trim())
      .map(c => ({ doctype: 'Possible Cause', cause_description: c.cause_description.trim() }))

    const effects = form.value.effects
      .filter(e => e.consequence_description?.trim())
      .map(e => ({ doctype: 'Risk Consequence', consequence_description: e.consequence_description.trim() }))

    const mitigatingActions = form.value.mitigating_actions
      .filter(a => a.action_description?.trim())
      .map(a => ({
        doctype: 'Mitigating Action',
        action_description: a.action_description.trim(),
        responsible_person: a.responsible_person || null,
        deadline: a.deadline || null,
        status: 'Pending',
        addresses_cause: a.addresses_cause || null
      }))

    const docData = {
      doctype: 'Program Risk Register',
      project: form.value.project || null,
      department: form.value.department,
      unit: form.value.unit || null,
      region: form.value.region || null,
      risk_category: form.value.risk_category,
      risk_type: form.value.risk_type || null,
      risk_owner: form.value.risk_owner || null,
      risk_description: form.value.risk_description,
      possible_causes: possibleCauses,
      effects,
      mitigating_actions: mitigatingActions,
      likelihood: form.value.likelihood,
      impact: form.value.impact,
      review_frequency: form.value.review_frequency || null,
      timeline: form.value.timeline || null,
      remarks: form.value.remarks || null,
      status: 'Draft'
    }

    const res = await axios.post('/api/resource/Program Risk Register', docData)

    if (res.data?.data) {
      const riskName = res.data.data.name

      // If submitting for approval, call the approval endpoint before navigating
      if (forApproval) {
        await api.submitForApproval(riskName)
      }

      if (addAnother) {
        // Keep step-1 basic info; reset only steps 2-3 fields
        form.value.risk_description = ''
        form.value.possible_causes = []
        form.value.effects = []
        form.value.mitigating_actions = []
        form.value.likelihood = 3
        form.value.impact = 3
        form.value.review_frequency = ''
        form.value.timeline = ''
        form.value.remarks = ''
        currentStep.value = 2
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } else {
        router.push(`/risk/${riskName}`)
      }
    } else {
      error.value = 'Failed to create risk. Please try again.'
    }
  } catch (err) {
    error.value = err.response?.data?.message || err.response?.data?.exc || 'An error occurred while creating the risk.'
  } finally {
    loading.value = false
    submitMode.value = ''
  }
}

// ── Load master data ──────────────────────────────────────────────────────────
const loadMasterData = async () => {
  try {
    const user = await api.getCurrentUser()
    currentUser.value = user

    const deptRes = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_departments')
    const depts = deptRes.data.message || []
    departments.value = depts
    allUnits.value = depts.flatMap(d => d.units || [])

    if (user?.department) {
      const userDept = depts.find(d => d.name === user.department)
      if (userDept) {
        form.value.department = userDept.name
        selectedDepartmentName.value = userDept.department_name
        departmentSearch.value = userDept.department_name
      }
    }

    const projRes = await axios.get('/api/resource/Project', {
      params: { fields: JSON.stringify(['name', 'project_name']), limit_page_length: 999 }
    })
    projects.value = projRes.data.data || []

    const regRes = await axios.get('/api/resource/Region', {
      params: { fields: JSON.stringify(['name', 'region_name']), limit_page_length: 999 }
    })
    regions.value = regRes.data.data || []
  } catch (err) {
    console.error('Failed to load master data', err)
  }
}

onMounted(() => loadMasterData())
</script>
