<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-elegant-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto animate-scale-in">
      <!-- Header -->
      <div class="sticky top-0 bg-white border-b border-light-border px-6 py-4 flex items-center justify-between">
        <h2 class="text-xl font-bold text-charcoal">{{ isEdit ? 'Edit Review' : 'Add New Review' }}</h2>
        <button @click="$emit('close')" class="text-medium-gray hover:text-charcoal">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
        <!-- Review Date & Reviewed By -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Review Date *</label>
            <input
              v-model="formData.review_date"
              type="date"
              required
              class="input"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-charcoal mb-2">Reviewed By *</label>
            <input
              v-model="formData.reviewed_by"
              type="text"
              required
              placeholder="Enter reviewer name"
              class="input"
            />
          </div>
        </div>

        <!-- Summary -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Summary of Review *</label>
          <textarea
            v-model="formData.summary"
            required
            rows="4"
            placeholder="Describe what was reviewed and key findings..."
            class="input resize-none"
          ></textarea>
        </div>

        <!-- Actions -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Decisions / Actions Agreed *</label>
          <textarea
            v-model="formData.actions"
            required
            rows="4"
            placeholder="List actions and decisions made during this review..."
            class="input resize-none"
          ></textarea>
        </div>

        <!-- Next Review Date -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-2">Next Review Date</label>
          <input
            v-model="formData.next_review_date"
            type="date"
            class="input"
          />
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="p-4 bg-red-light rounded-lg">
          <p class="text-sm text-red-dark">{{ errorMessage }}</p>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end space-x-3 pt-4 border-t border-light-border">
          <button
            type="button"
            @click="$emit('close')"
            class="btn btn-outline"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="btn btn-primary"
          >
            <span v-if="saving">Saving...</span>
            <span v-else>{{ isEdit ? 'Update Review' : 'Add Review' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  review: {
    type: Object,
    default: null
  },
  reviewIndex: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['close', 'submit'])

const isEdit = computed(() => props.review !== null)

const formData = ref({
  review_date: props.review?.review_date || '',
  reviewed_by: props.review?.reviewed_by || '',
  summary: props.review?.summary || '',
  actions: props.review?.actions || '',
  next_review_date: props.review?.next_review_date || ''
})

const saving = ref(false)
const errorMessage = ref('')

const handleSubmit = async () => {
  saving.value = true
  errorMessage.value = ''

  try {
    emit('submit', {
      data: formData.value,
      index: props.reviewIndex
    })
  } catch (error) {
    errorMessage.value = error.message || 'Failed to save review'
  } finally {
    saving.value = false
  }
}
</script>
