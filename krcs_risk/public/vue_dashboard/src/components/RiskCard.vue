<template>
  <div class="card hover:shadow-elegant-lg cursor-pointer" @click="$emit('click', risk)">
    <div class="flex items-start justify-between mb-3">
      <div class="flex-1">
        <h3 class="font-semibold text-charcoal mb-1">{{ risk.name }}</h3>
        <p class="text-sm text-medium-gray line-clamp-2">{{ risk.risk_description || 'No description' }}</p>
      </div>
      <span class="badge ml-3" :class="getBadgeClass(risk.risk_level)">
        {{ risk.risk_level || 'Unknown' }}
      </span>
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
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
