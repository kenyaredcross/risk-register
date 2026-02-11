<template>
  <div class="stat-card animate-slide-up" :class="animationDelay">
    <div class="w-12 h-12 rounded-full flex items-center justify-center mb-3" :class="iconBgClass">
      <slot name="icon">
        <svg class="w-6 h-6" :class="iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </slot>
    </div>
    <div class="stat-value" :class="valueClass">{{ value }}</div>
    <div class="stat-label">{{ label }}</div>
    <div v-if="subtitle" class="text-xs text-medium-gray mt-1">{{ subtitle }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: [String, Number],
    required: true
  },
  label: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'critical', 'high', 'medium', 'low'].includes(value)
  },
  delay: {
    type: Number,
    default: 0
  }
})

const iconBgClass = computed(() => {
  const variants = {
    default: 'bg-charcoal',
    critical: 'bg-red-primary',
    high: 'bg-orange-500',
    medium: 'bg-yellow-500',
    low: 'bg-green-500'
  }
  return variants[props.variant]
})

const iconClass = computed(() => {
  return 'text-white'
})

const valueClass = computed(() => {
  const variants = {
    default: 'text-charcoal',
    critical: 'text-red-primary',
    high: 'text-orange-600',
    medium: 'text-yellow-600',
    low: 'text-green-600'
  }
  return variants[props.variant]
})

const animationDelay = computed(() => {
  const delays = {
    0: '',
    100: 'animate-delay-100',
    200: 'animate-delay-200',
    300: 'animate-delay-300',
    400: 'animate-delay-400'
  }
  return delays[props.delay] || ''
})
</script>
