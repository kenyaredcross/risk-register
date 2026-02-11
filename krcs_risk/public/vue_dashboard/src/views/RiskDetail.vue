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
            <h1 class="text-3xl font-bold text-charcoal mb-2">{{ store.selectedRisk.name }}</h1>
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
                <span class="text-charcoal">{{ cause.cause }}</span>
              </li>
            </ul>
          </div>

          <!-- Consequences -->
          <div v-if="store.selectedRisk.risk_consequences && store.selectedRisk.risk_consequences.length > 0" class="card">
            <h2 class="card-header">Risk Consequences</h2>
            <ul class="space-y-2">
              <li v-for="(consequence, index) in store.selectedRisk.risk_consequences" :key="index" class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-red-primary mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <span class="text-charcoal">{{ consequence.effect }}</span>
              </li>
            </ul>
          </div>

          <!-- Mitigating Actions -->
          <div v-if="store.selectedRisk.mitigating_actions && store.selectedRisk.mitigating_actions.length > 0" class="card">
            <h2 class="card-header">Mitigating Actions</h2>
            <div class="space-y-3">
              <div v-for="(action, index) in store.selectedRisk.mitigating_actions" :key="index" class="p-4 bg-light-gray rounded-lg">
                <div class="font-semibold text-charcoal mb-2">{{ action.action }}</div>
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span class="text-medium-gray">Responsibility:</span>
                    <span class="ml-2 text-charcoal">{{ action.responsibility || 'N/A' }}</span>
                  </div>
                  <div>
                    <span class="text-medium-gray">Timeline:</span>
                    <span class="ml-2 text-charcoal">{{ action.timeline || 'N/A' }}</span>
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
                <div class="text-xs text-medium-gray mb-1">County</div>
                <div class="text-charcoal font-medium">{{ store.selectedRisk.county || 'N/A' }}</div>
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
    // Update existing review
    result = await api.updateRiskReview(riskName, index, data)
  } else {
    // Add new review
    result = await api.addRiskReview(riskName, data)
  }

  if (result.success) {
    // Reload the risk to get updated data
    await store.loadRisk(riskName)
    closeReviewForm()
  } else {
    alert(result.message || 'Failed to save review')
  }
}

onMounted(() => {
  const riskId = route.params.id
  store.loadRisk(riskId)
})
</script>
