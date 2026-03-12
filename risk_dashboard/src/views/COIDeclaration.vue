<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-charcoal mb-2">Conflict of Interest Declaration</h1>
      <p class="text-medium-gray">Submit your annual declaration or report a change in circumstances</p>
    </div>

    <!-- Form Card -->
    <div class="bg-white rounded-lg shadow-elegant p-6 md:p-8 max-w-4xl mx-auto">
      <form @submit.prevent="handleSubmit">

        <!-- Basic Information -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold text-charcoal mb-4">Basic Information</h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Employee Name (readonly, auto-filled) -->
            <div>
              <label class="block text-sm font-medium text-charcoal mb-2">Employee Name</label>
              <input
                v-model="form.employee_name"
                type="text"
                readonly
                class="input bg-gray-50 cursor-not-allowed"
              />
            </div>

            <!-- Department (readonly, auto-filled) -->
            <div>
              <label class="block text-sm font-medium text-charcoal mb-2">Department</label>
              <input
                v-model="form.department"
                type="text"
                readonly
                class="input bg-gray-50 cursor-not-allowed"
              />
            </div>

            <!-- Declaration Type -->
            <div>
              <label class="block text-sm font-medium text-charcoal mb-2">Type of Declaration *</label>
              <select v-model="form.declaration_type" required class="input">
                <option value="">Select...</option>
                <option value="Annual Declaration">Annual Declaration</option>
                <option value="Change in Circumstance">Change in Circumstance</option>
              </select>
            </div>

            <!-- Declaration Date (readonly, today) -->
            <div>
              <label class="block text-sm font-medium text-charcoal mb-2">Declaration Date</label>
              <input
                v-model="form.declaration_date"
                type="date"
                readonly
                class="input bg-gray-50 cursor-not-allowed"
              />
            </div>
          </div>
        </div>

        <!-- Q2-3: Financial Interests -->
        <div class="mb-8 pb-8 border-b border-light-border">
          <h3 class="text-lg font-semibold text-charcoal mb-4">Financial Interests</h3>

          <div class="mb-4">
            <label class="block text-sm font-medium text-charcoal mb-3">
              Do you or your immediate family members, close relatives, or friends have any financial interests, direct or indirect, in suppliers, contractors, sub-grantees, or other third-party contractors of the society? *
            </label>
            <div class="space-y-2">
              <label class="flex items-start">
                <input
                  v-model="form.has_financial_interests"
                  type="radio"
                  value="No, neither myself nor my immediate family members, close relatives, or friends have any financial interests."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">No, neither myself nor my immediate family members, close relatives, or friends have any financial interests.</span>
              </label>
              <label class="flex items-start">
                <input
                  v-model="form.has_financial_interests"
                  type="radio"
                  value="Yes, I and my immediate family members, close relatives, or friends have financial interests."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">Yes, I and my immediate family members, close relatives, or friends have financial interests.</span>
              </label>
            </div>
          </div>

          <div v-if="showFinancialDescription" class="mt-4">
            <label class="block text-sm font-medium text-charcoal mb-2">
              Describe the financial interests, direct or indirect, of suppliers, contractors, sub-grantees, or other third-party contractors of the Society. *
            </label>
            <textarea
              v-model="form.financial_interests_description"
              rows="4"
              required
              class="input resize-none"
              placeholder="Please provide detailed information..."
            ></textarea>
          </div>
        </div>

        <!-- Q4-5: Personal Relationships -->
        <div class="mb-8 pb-8 border-b border-light-border">
          <h3 class="text-lg font-semibold text-charcoal mb-4">Personal Relationships</h3>

          <div class="mb-4">
            <label class="block text-sm font-medium text-charcoal mb-3">
              Do you or your immediate family members, close relatives, or friends have any personal relationships with suppliers, contractors, sub-grantees, or other third-party contractors of the Society? *
            </label>
            <div class="space-y-2">
              <label class="flex items-start">
                <input
                  v-model="form.has_personal_relationships"
                  type="radio"
                  value="No, neither myself nor my immediate family members, close relatives, or friends have any personal relationships."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">No, neither myself nor my immediate family members, close relatives, or friends have any personal relationships.</span>
              </label>
              <label class="flex items-start">
                <input
                  v-model="form.has_personal_relationships"
                  type="radio"
                  value="Yes, I and my immediate family members, close relatives, or friends have personal relationships."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">Yes, I and my immediate family members, close relatives, or friends have personal relationships.</span>
              </label>
            </div>
          </div>

          <div v-if="showPersonalDescription" class="mt-4">
            <label class="block text-sm font-medium text-charcoal mb-2">
              Describe the personal relationships with suppliers, contractors, sub-grantees, or other third-party contractors of the Society. *
            </label>
            <textarea
              v-model="form.personal_relationships_description"
              rows="4"
              required
              class="input resize-none"
              placeholder="Please provide detailed information..."
            ></textarea>
          </div>
        </div>

        <!-- Q6-7: Supervisory Roles -->
        <div class="mb-8 pb-8 border-b border-light-border">
          <h3 class="text-lg font-semibold text-charcoal mb-4">Supervisory Roles</h3>

          <div class="mb-4">
            <label class="block text-sm font-medium text-charcoal mb-3">
              Do you or your family members or relatives have supervisory roles in Kenya Red Cross Society over each other? *
            </label>
            <div class="space-y-2">
              <label class="flex items-start">
                <input
                  v-model="form.has_supervisory_roles"
                  type="radio"
                  value="No, neither I nor my family members/relatives have supervisory roles in Kenya Red Cross Society over each other."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">No, neither I nor my family members/relatives have supervisory roles in Kenya Red Cross Society over each other.</span>
              </label>
              <label class="flex items-start">
                <input
                  v-model="form.has_supervisory_roles"
                  type="radio"
                  value="Yes, I and my family members or relatives have supervisory roles in Kenya Red Cross Society over each other."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">Yes, I and my family members or relatives have supervisory roles in Kenya Red Cross Society over each other.</span>
              </label>
            </div>
          </div>

          <div v-if="showSupervisoryDescription" class="mt-4">
            <label class="block text-sm font-medium text-charcoal mb-2">
              Describe the supervisory roles at Kenya Red Cross Society that you or any of your family members or relatives have over each other. *
            </label>
            <textarea
              v-model="form.supervisory_roles_description"
              rows="4"
              required
              class="input resize-none"
              placeholder="Please provide detailed information..."
            ></textarea>
          </div>
        </div>

        <!-- Q8-9: Other Organizational Roles -->
        <div class="mb-8 pb-8 border-b border-light-border">
          <h3 class="text-lg font-semibold text-charcoal mb-4">Other Organizational Roles</h3>

          <div class="mb-4">
            <label class="block text-sm font-medium text-charcoal mb-3">
              I do not hold any trusteeship, directorship, or employment roles in any other organization. *
            </label>
            <div class="space-y-2">
              <label class="flex items-start">
                <input
                  v-model="form.has_other_roles"
                  type="radio"
                  value="No, I do not hold any trusteeship, directorship, or employment roles in any other organization."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">No, I do not hold any trusteeship, directorship, or employment roles in any other organization.</span>
              </label>
              <label class="flex items-start">
                <input
                  v-model="form.has_other_roles"
                  type="radio"
                  value="Yes, I do hold trusteeship, directorship, or employment roles in other organizations."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">Yes, I do hold trusteeship, directorship, or employment roles in other organizations.</span>
              </label>
            </div>
          </div>

          <div v-if="showOtherRolesDescription" class="mt-4">
            <label class="block text-sm font-medium text-charcoal mb-2">
              Describe the trusteeship, directorship, or employment role you have in any other organization. *
            </label>
            <textarea
              v-model="form.other_roles_description"
              rows="4"
              required
              class="input resize-none"
              placeholder="Please provide detailed information..."
            ></textarea>
          </div>
        </div>

        <!-- Q10-11: Public Office -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold text-charcoal mb-4">Public Office</h3>

          <div class="mb-4">
            <label class="block text-sm font-medium text-charcoal mb-3">
              I am not running for or plan to run for public office in the foreseeable future. *
            </label>
            <div class="space-y-2">
              <label class="flex items-start">
                <input
                  v-model="form.plans_public_office"
                  type="radio"
                  value="No, I am not running for or plan to run for public office in the foreseeable future."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">No, I am not running for or plan to run for public office in the foreseeable future.</span>
              </label>
              <label class="flex items-start">
                <input
                  v-model="form.plans_public_office"
                  type="radio"
                  value="Yes, I am running for or plan to run for public office in the foreseeable future."
                  class="mt-1 mr-3"
                  required
                />
                <span class="text-sm">Yes, I am running for or plan to run for public office in the foreseeable future.</span>
              </label>
            </div>
          </div>

          <div v-if="showPublicOfficeDescription" class="mt-4">
            <label class="block text-sm font-medium text-charcoal mb-2">
              Describe which public office you are running for or plan to run for in the foreseeable future. *
            </label>
            <textarea
              v-model="form.public_office_description"
              rows="4"
              required
              class="input resize-none"
              placeholder="Please provide detailed information..."
            ></textarea>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-light rounded-lg">
          <p class="text-sm text-red-dark">{{ errorMessage }}</p>
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="mb-6 p-4 bg-green-100 rounded-lg">
          <p class="text-sm text-green-700">{{ successMessage }}</p>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center justify-end space-x-4 pt-6 border-t border-light-border">
          <button
            type="button"
            @click="saveDraft"
            :disabled="saving"
            class="btn btn-outline"
          >
            <span v-if="saving && !submitting">Saving Draft...</span>
            <span v-else>Save as Draft</span>
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="btn btn-primary"
          >
            <span v-if="saving && submitting">Submitting...</span>
            <span v-else>Submit Declaration</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Form data
const form = ref({
  employee: '',
  employee_name: '',
  department: '',
  designation: '',
  declaration_type: '',
  declaration_date: getTodayDate(),
  has_financial_interests: '',
  financial_interests_description: '',
  has_personal_relationships: '',
  personal_relationships_description: '',
  has_supervisory_roles: '',
  supervisory_roles_description: '',
  has_other_roles: '',
  other_roles_description: '',
  plans_public_office: '',
  public_office_description: ''
})

const saving = ref(false)
const submitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Computed properties for conditional field visibility
const showFinancialDescription = computed(() =>
  form.value.has_financial_interests && form.value.has_financial_interests.startsWith('Yes')
)

const showPersonalDescription = computed(() =>
  form.value.has_personal_relationships && form.value.has_personal_relationships.startsWith('Yes')
)

const showSupervisoryDescription = computed(() =>
  form.value.has_supervisory_roles && form.value.has_supervisory_roles.startsWith('Yes')
)

const showOtherRolesDescription = computed(() =>
  form.value.has_other_roles && form.value.has_other_roles.startsWith('Yes')
)

const showPublicOfficeDescription = computed(() =>
  form.value.plans_public_office && form.value.plans_public_office.startsWith('Yes')
)

// Helper function to get today's date
function getTodayDate() {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// Load user's employee data
const loadEmployeeData = async () => {
  try {
    const response = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.conflict_of_interest_declaration.api.get_user_employee')

    if (response.data.message) {
      const employee = response.data.message
      form.value.employee = employee.name
      form.value.employee_name = employee.employee_name
      form.value.department = employee.department
      form.value.designation = employee.designation
    } else {
      errorMessage.value = 'No employee record found for your user account. Please contact your administrator.'
    }
  } catch (error) {
    console.error('Error loading employee data:', error)
    errorMessage.value = 'Failed to load employee information'
  }
}

// Save as draft
const saveDraft = async () => {
  saving.value = true
  submitting.value = false
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const data = {
      employee: form.value.employee,
      declaration_type: form.value.declaration_type,
      declaration_date: form.value.declaration_date,
      has_financial_interests: form.value.has_financial_interests,
      financial_interests_description: form.value.financial_interests_description,
      has_personal_relationships: form.value.has_personal_relationships,
      personal_relationships_description: form.value.personal_relationships_description,
      has_supervisory_roles: form.value.has_supervisory_roles,
      supervisory_roles_description: form.value.supervisory_roles_description,
      has_other_roles: form.value.has_other_roles,
      other_roles_description: form.value.other_roles_description,
      plans_public_office: form.value.plans_public_office,
      public_office_description: form.value.public_office_description,
      status: 'Draft',
      submit: false
    }

    const response = await axios.post(
      '/api/method/krcs_risk.krcs_risk_management.doctype.conflict_of_interest_declaration.api.create_declaration',
      { data: JSON.stringify(data) }
    )

    if (response.data.message.success) {
      successMessage.value = 'Draft saved successfully!'
      setTimeout(() => {
        router.push('/coi-declarations')
      }, 1500)
    }
  } catch (error) {
    console.error('Error saving draft:', error)
    errorMessage.value = error.response?.data?.message || 'Failed to save draft'
  } finally {
    saving.value = false
  }
}

// Submit declaration
const handleSubmit = async () => {
  saving.value = true
  submitting.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const data = {
      employee: form.value.employee,
      declaration_type: form.value.declaration_type,
      declaration_date: form.value.declaration_date,
      has_financial_interests: form.value.has_financial_interests,
      financial_interests_description: form.value.financial_interests_description,
      has_personal_relationships: form.value.has_personal_relationships,
      personal_relationships_description: form.value.personal_relationships_description,
      has_supervisory_roles: form.value.has_supervisory_roles,
      supervisory_roles_description: form.value.supervisory_roles_description,
      has_other_roles: form.value.has_other_roles,
      other_roles_description: form.value.other_roles_description,
      plans_public_office: form.value.plans_public_office,
      public_office_description: form.value.public_office_description,
      status: 'Submitted',
      submit: true
    }

    const response = await axios.post(
      '/api/method/krcs_risk.krcs_risk_management.doctype.conflict_of_interest_declaration.api.create_declaration',
      { data: JSON.stringify(data) }
    )

    if (response.data.message.success) {
      successMessage.value = 'Declaration submitted successfully!'
      setTimeout(() => {
        router.push('/coi-declarations')
      }, 1500)
    }
  } catch (error) {
    console.error('Error submitting declaration:', error)
    errorMessage.value = error.response?.data?.message || 'Failed to submit declaration'
  } finally {
    saving.value = false
    submitting.value = false
  }
}

// Load employee data on mount
onMounted(() => {
  loadEmployeeData()
})
</script>
