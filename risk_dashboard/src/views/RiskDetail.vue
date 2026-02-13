<template>
  <div class="animate-fade-in">
    <!-- Loading State -->
    <div v-if="store.loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-primary"></div>
    </div>

    <!-- Risk Detail -->
    <div v-else-if="store.selectedRisk">
      <!-- Header -->
      <div class="mb-6">
        <button @click="router.back()" class="text-medium-gray hover:text-charcoal mb-4 flex items-center space-x-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          <span>Back</span>
        </button>

        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-3xl font-bold text-charcoal mb-1">{{ store.selectedRisk.project || store.selectedRisk.name }}</h1>
            <p class="text-sm text-medium-gray font-mono mb-1">{{ store.selectedRisk.name }}</p>
            <p class="text-medium-gray">{{ formatDate(store.selectedRisk.creation) }}</p>
          </div>
          <span class="badge text-base px-4 py-2" :class="getBadgeClass(store.selectedRisk.risk_level)">
            {{ store.selectedRisk.risk_level || 'Unknown' }}
          </span>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column (2/3) -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Description -->
          <div class="card">
            <h2 class="card-header">Risk Description</h2>
            <p class="text-charcoal">{{ store.selectedRisk.risk_description || 'No description available' }}</p>
          </div>

          <!-- Risk Assessment -->
          <div class="card">
            <h2 class="card-header">Risk Assessment</h2>
            <div class="grid grid-cols-3 gap-6">
              <div class="text-center p-4 bg-light-gray rounded-lg">
                <div class="text-sm text-medium-gray mb-2">Likelihood</div>
                <div class="text-4xl font-bold text-charcoal">{{ store.selectedRisk.likelihood || 0 }}</div>
                <div class="text-xs text-medium-gray mt-1">out of 5</div>
              </div>
              <div class="text-center p-4 bg-light-gray rounded-lg">
                <div class="text-sm text-medium-gray mb-2">Impact</div>
                <div class="text-4xl font-bold text-charcoal">{{ store.selectedRisk.impact || 0 }}</div>
                <div class="text-xs text-medium-gray mt-1">out of 5</div>
              </div>
              <div class="text-center p-4 rounded-lg" :class="getRatingBgClass(store.selectedRisk.overall_rating)">
                <div class="text-sm mb-2" :class="getRatingTextClass(store.selectedRisk.overall_rating)">Overall Rating</div>
                <div class="text-4xl font-bold" :class="getRatingTextClass(store.selectedRisk.overall_rating)">
                  {{ store.selectedRisk.overall_rating || 0 }}
                </div>
                <div class="text-xs mt-1" :class="getRatingTextClass(store.selectedRisk.overall_rating)">Likelihood × Impact</div>
              </div>
            </div>
          </div>

          <!-- Possible Causes -->
          <div v-if="store.selectedRisk.possible_causes && store.selectedRisk.possible_causes.length > 0" class="card">
            <h2 class="card-header">Possible Causes</h2>
            <ul class="space-y-2">
              <li v-for="(cause, index) in store.selectedRisk.possible_causes" :key="index" class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-red-primary mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
                <span class="text-charcoal">{{ cause.cause_description }}</span>
              </li>
            </ul>
          </div>

          <!-- Consequences -->
          <div v-if="store.selectedRisk.effects && store.selectedRisk.effects.length > 0" class="card">
            <h2 class="card-header">Risk Consequences</h2>
            <ul class="space-y-2">
              <li v-for="(consequence, index) in store.selectedRisk.effects" :key="index" class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-red-primary mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <span class="text-charcoal">{{ consequence.consequence_description }}</span>
              </li>
            </ul>
          </div>

          <!-- Mitigating Actions -->
          <div v-if="store.selectedRisk.mitigating_actions && store.selectedRisk.mitigating_actions.length > 0" class="card">
            <h2 class="card-header">Mitigating Actions</h2>
            <div class="space-y-3">
              <div v-for="(action, index) in store.selectedRisk.mitigating_actions" :key="index" class="p-4 bg-light-gray rounded-lg">
                <div class="font-semibold text-charcoal mb-2">{{ action.action_description }}</div>
                <div class="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span class="text-medium-gray">Responsible Person:</span>
                    <span class="ml-2 text-charcoal">{{ action.responsible_person || 'N/A' }}</span>
                  </div>
                  <div>
                    <span class="text-medium-gray">Deadline:</span>
                    <span class="ml-2 text-charcoal">{{ action.deadline || 'N/A' }}</span>
                  </div>
                  <div>
                    <span class="text-medium-gray">Status:</span>
                    <span class="ml-2 text-charcoal">
                      <span
                        class="px-2 py-0.5 rounded-full text-xs font-semibold"
                        :class="{
                          'bg-yellow-100 text-yellow-700': action.status === 'Pending',
                          'bg-blue-100 text-blue-700': action.status === 'In Progress',
                          'bg-green-100 text-green-700': action.status === 'Completed',
                          'bg-gray-100 text-gray-600': action.status === 'Cancelled'
                        }"
                      >
                        {{ action.status || 'Pending' }}
                      </span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Risk Reviews Timeline -->
          <div class="card">
            <div class="flex items-center justify-between mb-6">
              <h2 class="card-header mb-0">Risk Reviews</h2>
              <button @click="openReviewForm()" class="btn btn-danger text-sm">
                Add Review
              </button>
            </div>

            <div v-if="store.selectedRisk.risk_reviews && store.selectedRisk.risk_reviews.length > 0" class="relative">
              <!-- Timeline line -->
              <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-light-gray"></div>

              <!-- Timeline items -->
              <div class="space-y-8">
                <div v-for="(review, index) in store.selectedRisk.risk_reviews" :key="index" class="relative pl-12">
                  <!-- Timeline dot -->
                  <div class="absolute left-2.5 top-1 w-3 h-3 rounded-full bg-red-primary ring-4 ring-white"></div>

                  <!-- Review content -->
                  <div class="bg-light-gray rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div class="flex items-start justify-between mb-3">
                      <div>
                        <div class="font-bold text-charcoal text-lg">{{ formatDate(review.review_date) }}</div>
                        <div class="text-sm text-medium-gray flex items-center mt-1">
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                          {{ review.reviewed_by }}
                        </div>
                      </div>
                      <button @click="openReviewForm(review, index)" class="text-medium-gray hover:text-red-primary transition-colors" title="Edit">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                    </div>

                    <div v-if="review.summary" class="mb-3">
                      <div class="text-xs font-bold text-medium-gray uppercase tracking-wide mb-1">Summary</div>
                      <div class="text-sm text-charcoal whitespace-pre-wrap leading-relaxed">{{ review.summary }}</div>
                    </div>

                    <div v-if="review.actions" class="mb-3">
                      <div class="text-xs font-bold text-medium-gray uppercase tracking-wide mb-1">Actions Agreed</div>
                      <div class="text-sm text-charcoal whitespace-pre-wrap leading-relaxed">{{ review.actions }}</div>
                    </div>

                    <div v-if="review.next_review_date" class="flex items-center text-xs text-medium-gray mt-3 pt-3 border-t border-white">
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      Next Review: {{ formatDate(review.next_review_date) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-12 text-medium-gray">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-light-gray flex items-center justify-center">
                <svg class="w-8 h-8 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p class="font-medium">No reviews yet</p>
              <p class="text-sm mt-1">Click "Add Review" to create the first review</p>
            </div>
          </div>
        </div>

        <!-- Right Column (1/3) -->
        <div class="space-y-6">
          <!-- Quick Info -->
          <div class="card">
            <h2 class="card-header">Quick Info</h2>
            <div class="space-y-4">
              <div>
                <div class="text-xs text-medium-gray mb-1">Risk Category</div>
                <div class="text-charcoal font-medium">{{ store.selectedRisk.risk_category || 'N/A' }}</div>
              </div>
              <div>
                <div class="text-xs text-medium-gray mb-1">Risk Owner</div>
                <div class="text-charcoal font-medium">{{ store.selectedRisk.risk_owner || 'Unassigned' }}</div>
              </div>
              <div>
                <div class="text-xs text-medium-gray mb-1">Department</div>
                <div class="text-charcoal font-medium">{{ store.selectedRisk.department || 'N/A' }}</div>
              </div>
              <div>
                <div class="text-xs text-medium-gray mb-1">Unit</div>
                <div class="text-charcoal font-medium">{{ store.selectedRisk.unit || 'N/A' }}</div>
              </div>
              <div>
                <div class="text-xs text-medium-gray mb-1">Region</div>
                <div class="text-charcoal font-medium">{{ store.selectedRisk.region || 'N/A' }}</div>
              </div>
              <div>
                <div class="text-xs text-medium-gray mb-1">Status</div>
                <span class="badge badge-medium">{{ store.selectedRisk.status || 'Unknown' }}</span>
              </div>
              <div>
                <div class="text-xs text-medium-gray mb-1">Timeline</div>
                <div class="text-charcoal font-medium">{{ store.selectedRisk.timeline || 'N/A' }}</div>
              </div>
            </div>
          </div>

          <!-- Review Schedule -->
          <div class="card">
            <h2 class="card-header">Review Schedule</h2>
            <div class="space-y-4">
              <div>
                <div class="text-xs text-medium-gray mb-1">Frequency</div>
                <div class="text-charcoal font-medium">{{ store.selectedRisk.review_frequency || 'Not Set' }}</div>
              </div>
              <div>
                <div class="text-xs text-medium-gray mb-1">Next Review Due</div>
                <div class="text-charcoal font-medium">{{ store.selectedRisk.next_review_due || 'N/A' }}</div>
              </div>
              <div>
                <div class="text-xs text-medium-gray mb-1">Review Status</div>
                <span class="px-2 py-1 rounded-full text-xs font-semibold" :class="getReviewStatusClass(store.selectedRisk.review_status)">
                  {{ store.selectedRisk.review_status || 'Not Scheduled' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Timestamps -->
          <div class="card">
            <h2 class="card-header">Timeline</h2>
            <div class="space-y-3">
              <div>
                <div class="text-xs text-medium-gray mb-1">Created</div>
                <div class="text-sm text-charcoal">{{ formatDate(store.selectedRisk.creation) }}</div>
              </div>
              <div>
                <div class="text-xs text-medium-gray mb-1">Last Modified</div>
                <div class="text-sm text-charcoal">{{ formatDate(store.selectedRisk.modified) }}</div>
              </div>
            </div>
          </div>

          <!-- Approval Status -->
          <div class="card">
            <h2 class="card-header">Approval</h2>
            <div class="space-y-4">
              <div>
                <div class="text-xs text-medium-gray mb-1">Workflow Status</div>
                <span class="px-3 py-1 rounded-full text-xs font-semibold" :class="getStatusClass(store.selectedRisk.status)">
                  {{ store.selectedRisk.status || 'Draft' }}
                </span>
              </div>
              <div v-if="store.selectedRisk.approved_by">
                <div class="text-xs text-medium-gray mb-1">{{ store.selectedRisk.status === 'Rejected' ? 'Rejected By' : 'Approved By' }}</div>
                <div class="text-charcoal font-medium text-sm">{{ store.selectedRisk.approved_by }}</div>
              </div>
              <div v-if="store.selectedRisk.approval_date">
                <div class="text-xs text-medium-gray mb-1">Date</div>
                <div class="text-charcoal font-medium text-sm">{{ formatDate(store.selectedRisk.approval_date) }}</div>
              </div>
              <div v-if="store.selectedRisk.rejection_reason">
                <div class="text-xs text-medium-gray mb-1">Rejection Reason</div>
                <div class="text-sm text-red-700 bg-red-50 rounded p-2">{{ store.selectedRisk.rejection_reason }}</div>
              </div>

              <!-- Workflow Action Buttons -->
              <div class="space-y-2 pt-2 border-t border-light-border">
                <!-- Submit for Approval: Draft or Rejected -->
                <button
                  v-if="store.selectedRisk.status === 'Draft' || store.selectedRisk.status === 'Rejected'"
                  @click="handleSubmitForApproval"
                  :disabled="actionLoading"
                  class="btn btn-primary w-full text-sm"
                >
                  {{ actionLoading ? 'Submitting...' : 'Submit for Approval' }}
                </button>

                <!-- Request Closure: Open -->
                <button
                  v-if="store.selectedRisk.status === 'Open'"
                  @click="handleRequestClose"
                  :disabled="actionLoading"
                  class="btn btn-outline w-full text-sm"
                >
                  {{ actionLoading ? 'Requesting...' : 'Request Closure' }}
                </button>

                <!-- Approve (Approver only) -->
                <button
                  v-if="isApprover && (store.selectedRisk.status === 'Pending Approval' || store.selectedRisk.status === 'Pending Close Approval')"
                  @click="handleApprove"
                  :disabled="actionLoading"
                  class="btn btn-primary w-full text-sm"
                >
                  {{ actionLoading ? 'Approving...' : 'Approve' }}
                </button>

                <!-- Reject (Approver only) -->
                <button
                  v-if="isApprover && (store.selectedRisk.status === 'Pending Approval' || store.selectedRisk.status === 'Pending Close Approval')"
                  @click="showRejectModal = true"
                  :disabled="actionLoading"
                  class="w-full px-4 py-2 border border-red-primary text-red-primary rounded-lg hover:bg-red-50 transition-colors text-sm font-medium"
                >
                  Reject
                </button>

                <div v-if="actionError" class="text-xs text-red-600 mt-1">{{ actionError }}</div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="card">
            <h2 class="card-header">Actions</h2>
            <div class="space-y-2">
              <a :href="`/app/program-risk-register/${store.selectedRisk.name}`" target="_blank" class="btn btn-primary w-full block text-center">
                Edit in Frappe
              </a>
              <button @click="router.push('/risks')" class="btn btn-outline w-full">
                View All Risks
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found -->
    <div v-else class="card text-center py-12">
      <svg class="w-16 h-16 text-medium-gray mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-medium-gray mb-4">Risk not found</p>
      <button @click="router.push('/risks')" class="btn btn-outline">
        Back to Risk Register
      </button>
    </div>

    <!-- Review Form Modal -->
    <ReviewForm
      v-if="showReviewForm"
      :review="currentReview"
      :review-index="currentReviewIndex"
      @close="closeReviewForm"
      @submit="handleReviewSubmit"
    />

    <!-- Reject Modal -->
    <div v-if="showRejectModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="showRejectModal = false">
      <div class="bg-white rounded-lg shadow-elegant-xl max-w-md w-full p-6">
        <h3 class="text-lg font-bold text-charcoal mb-4">Reject Risk</h3>
        <label class="block text-sm font-medium text-charcoal mb-2">Rejection Reason <span class="text-red-primary">*</span></label>
        <textarea
          v-model="rejectReason"
          rows="3"
          placeholder="Provide a reason for rejection..."
          class="input w-full mb-4"
        ></textarea>
        <div v-if="actionError" class="text-sm text-red-600 mb-3">{{ actionError }}</div>
        <div class="flex space-x-3">
          <button @click="showRejectModal = false" class="btn btn-outline flex-1">Cancel</button>
          <button @click="handleReject" :disabled="!rejectReason.trim() || actionLoading" class="flex-1 px-4 py-2 bg-red-primary text-white rounded-lg hover:bg-red-dark disabled:opacity-50 font-medium">
            {{ actionLoading ? 'Rejecting...' : 'Confirm Reject' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRiskStore } from '../stores/riskStore'
import { useApi } from '../composables/useApi'
import ReviewForm from '../components/ReviewForm.vue'

const route = useRoute()
const router = useRouter()
const store = useRiskStore()
const api = useApi()

const showReviewForm = ref(false)
const currentReview = ref(null)
const currentReviewIndex = ref(null)

// Approval state
const isApprover = ref(false)
const actionLoading = ref(false)
const actionError = ref('')
const showRejectModal = ref(false)
const rejectReason = ref('')

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getBadgeClass = (level) => {
  const levelMap = {
    'low': 'badge-low',
    'medium': 'badge-medium',
    'high': 'badge-high',
    'critical': 'badge-critical'
  }
  return levelMap[(level || '').toLowerCase()] || 'badge-medium'
}

const getReviewStatusClass = (status) => {
  const map = {
    'Overdue':       'bg-red-100 text-red-700',
    'Due Soon':      'bg-yellow-100 text-yellow-700',
    'On Track':      'bg-green-100 text-green-700',
    'Not Scheduled': 'bg-gray-100 text-gray-500',
  }
  return map[status] || 'bg-gray-100 text-gray-500'
}

const getRatingBgClass = (rating) => {
  if (rating >= 15) return 'bg-red-light'
  if (rating >= 10) return 'bg-orange-100'
  if (rating >= 5) return 'bg-yellow-100'
  return 'bg-green-100'
}

const getRatingTextClass = (rating) => {
  if (rating >= 15) return 'text-red-dark'
  if (rating >= 10) return 'text-orange-800'
  if (rating >= 5) return 'text-yellow-800'
  return 'text-green-800'
}

const openReviewForm = (review = null, index = null) => {
  currentReview.value = review
  currentReviewIndex.value = index
  showReviewForm.value = true
}

const closeReviewForm = () => {
  showReviewForm.value = false
  currentReview.value = null
  currentReviewIndex.value = null
}

const handleReviewSubmit = async ({ data, index }) => {
  const riskName = store.selectedRisk.name

  let result
  if (index !== null) {
    result = await api.updateRiskReview(riskName, index, data)
  } else {
    result = await api.addRiskReview(riskName, data)
  }

  if (result.success) {
    await store.loadRisk(riskName)
    closeReviewForm()
  } else {
    alert(result.message || 'Failed to save review')
  }
}

// --- Approval helpers ---

const getStatusClass = (status) => {
  const map = {
    'Draft':                   'bg-gray-100 text-gray-600',
    'Pending Approval':        'bg-orange-100 text-orange-700',
    'Open':                    'bg-green-100 text-green-700',
    'Pending Close Approval':  'bg-orange-100 text-orange-700',
    'Closed':                  'bg-blue-100 text-blue-700',
    'Rejected':                'bg-red-100 text-red-700',
  }
  return map[status] || 'bg-gray-100 text-gray-600'
}

const handleSubmitForApproval = async () => {
  actionLoading.value = true
  actionError.value = ''
  const result = await api.submitForApproval(store.selectedRisk.name)
  actionLoading.value = false
  if (result.success) {
    await store.loadRisk(store.selectedRisk.name)
  } else {
    actionError.value = result.message || 'Failed to submit.'
  }
}

const handleRequestClose = async () => {
  actionLoading.value = true
  actionError.value = ''
  const result = await api.requestClose(store.selectedRisk.name)
  actionLoading.value = false
  if (result.success) {
    await store.loadRisk(store.selectedRisk.name)
  } else {
    actionError.value = result.message || 'Failed to request closure.'
  }
}

const handleApprove = async () => {
  actionLoading.value = true
  actionError.value = ''
  const result = await api.approveRisk(store.selectedRisk.name)
  actionLoading.value = false
  if (result.success) {
    await store.loadRisk(store.selectedRisk.name)
  } else {
    actionError.value = result.message || 'Failed to approve.'
  }
}

const handleReject = async () => {
  if (!rejectReason.value.trim()) return
  actionLoading.value = true
  actionError.value = ''
  const result = await api.rejectRisk(store.selectedRisk.name, rejectReason.value)
  actionLoading.value = false
  if (result.success) {
    showRejectModal.value = false
    rejectReason.value = ''
    await store.loadRisk(store.selectedRisk.name)
  } else {
    actionError.value = result.message || 'Failed to reject.'
  }
}

onMounted(async () => {
  const riskId = route.params.id
  await store.loadRisk(riskId)
  // Check per-risk approval eligibility (scoped: HOD=dept, PM=project, HOR/DSG=global)
  const approvalInfo = await api.canApproveRisk(riskId)
  isApprover.value = approvalInfo.can_approve
})
</script>
