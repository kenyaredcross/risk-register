<template>
  <div class="card hover:shadow-elegant-lg cursor-pointer" @click="$emit('click', risk)">
    <div class="flex items-start justify-between mb-3">
      <div class="flex-1">
        <h3 class="font-semibold text-charcoal mb-0.5">{{ risk.project || risk.name }}</h3>
        <p class="text-xs text-medium-gray font-mono mb-1">{{ risk.name }}</p>
        <p class="text-sm text-medium-gray line-clamp-2">{{ risk.risk_description || 'No description' }}</p>
      </div>
      <div class="flex flex-col items-end space-y-1 ml-3">
        <span class="badge" :class="getBadgeClass(risk.risk_level)">
          {{ risk.risk_level || 'Unknown' }}
        </span>
        <span v-if="risk.risk_category" class="text-xs px-2 py-0.5 rounded-full bg-light-gray text-charcoal font-medium whitespace-nowrap">
          {{ risk.risk_category }}
        </span>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-light-border">
      <!-- Likelihood -->
      <div class="text-center">
        <div class="text-xs text-medium-gray mb-1">Likelihood</div>
        <div class="text-lg font-bold text-charcoal">{{ risk.likelihood || 0 }}</div>
      </div>

      <!-- Impact -->
      <div class="text-center">
        <div class="text-xs text-medium-gray mb-1">Impact</div>
        <div class="text-lg font-bold text-charcoal">{{ risk.impact || 0 }}</div>
      </div>

      <!-- Rating -->
      <div class="text-center">
        <div class="text-xs text-medium-gray mb-1">Rating</div>
        <div class="text-lg font-bold" :class="getRatingClass(risk.overall_rating)">
          {{ risk.overall_rating || 0 }}
        </div>
      </div>
    </div>

    <div class="mt-4 pt-4 border-t border-light-border flex items-center justify-between text-xs text-medium-gray">
      <div class="flex items-center space-x-1">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span>{{ risk.risk_owner || 'Unassigned' }}</span>
      </div>
      <div class="flex items-center space-x-1">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <span>{{ risk.department || 'N/A' }}</span>
      </div>
    </div>

    <!-- Review Status Bar -->
    <div v-if="risk.review_frequency" class="mt-3 pt-3 border-t border-light-border flex items-center justify-between text-xs">
      <div class="flex items-center space-x-1 text-medium-gray">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ risk.review_frequency }}</span>
        <span v-if="risk.next_review_due" class="text-charcoal">· Due {{ risk.next_review_due }}</span>
      </div>
      <span class="px-2 py-0.5 rounded-full font-semibold text-xs" :class="getReviewStatusClass(risk.review_status)">
        {{ risk.review_status || 'Not Scheduled' }}
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  risk: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

const getBadgeClass = (level) => {
  const levelMap = {
    'low': 'badge-low',
    'medium': 'badge-medium',
    'high': 'badge-high',
    'critical': 'badge-critical'
  }
  return levelMap[(level || '').toLowerCase()] || 'badge-medium'
}

const getRatingClass = (rating) => {
  if (rating >= 15) return 'text-red-primary'
  if (rating >= 10) return 'text-orange-600'
  if (rating >= 5) return 'text-yellow-600'
  return 'text-green-600'
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
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
