<template>
  <div class="card">
    <h2 class="card-header flex items-center justify-between">
      <span>Risk Matrix</span>
      <span class="text-sm font-normal text-medium-gray">Likelihood × Impact</span>
    </h2>

    <div class="overflow-x-auto">
      <div class="inline-block min-w-full">
        <!-- Matrix Grid -->
        <div class="flex">
          <!-- Y-axis label (Impact) -->
          <div class="flex flex-col justify-center pr-4">
            <div class="writing-mode-vertical text-sm font-semibold text-medium-gray uppercase tracking-wide">
              Impact
            </div>
          </div>

          <!-- Matrix -->
          <div class="flex-1">
            <!-- Impact labels (5 to 1) -->
            <div class="flex mb-2">
              <div class="w-12"></div>
              <div class="flex-1 grid grid-cols-5 gap-2 text-center">
                <div v-for="i in 5" :key="`impact-${i}`" class="text-xs font-semibold text-medium-gray">
                  {{ 6 - i }}
                </div>
              </div>
            </div>

            <!-- Matrix cells -->
            <div class="space-y-2">
              <div v-for="(row, rowIndex) in matrix" :key="`row-${rowIndex}`" class="flex gap-2">
                <!-- Row label (Impact value) -->
                <div class="w-12 flex items-center justify-center text-xs font-semibold text-medium-gray">
                  {{ 5 - rowIndex }}
                </div>

                <!-- Cells -->
                <div class="flex-1 grid grid-cols-5 gap-2">
                  <div
                    v-for="(count, colIndex) in row"
                    :key="`cell-${rowIndex}-${colIndex}`"
                    @click="onCellClick(rowIndex, colIndex)"
                    class="aspect-square flex items-center justify-center rounded-lg cursor-pointer transition-all duration-200 hover:scale-105"
                    :class="getCellClass(rowIndex, colIndex)"
                    :title="getCellTitle(rowIndex, colIndex, count)"
                  >
                    <span class="text-lg font-bold" :class="count > 0 ? 'text-white' : 'text-gray-400'">
                      {{ count || '0' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Likelihood labels (1 to 5) -->
            <div class="flex mt-2">
              <div class="w-12"></div>
              <div class="flex-1 grid grid-cols-5 gap-2 text-center">
                <div v-for="i in 5" :key="`likelihood-${i}`" class="text-xs font-semibold text-medium-gray">
                  {{ i }}
                </div>
              </div>
            </div>

            <!-- X-axis label -->
            <div class="text-center mt-4">
              <div class="text-sm font-semibold text-medium-gray uppercase tracking-wide">
                Likelihood
              </div>
            </div>
          </div>
        </div>

        <!-- Legend -->
        <div class="mt-6 flex flex-wrap gap-4 justify-center">
          <div v-for="level in riskLevels" :key="level.label" class="flex items-center space-x-2">
            <div class="w-4 h-4 rounded" :class="level.class"></div>
            <span class="text-sm font-medium">{{ level.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  matrix: {
    type: Array,
    required: true
  },
  risksByCell: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['cell-click'])

const riskLevels = [
  { label: 'Low (1-4)', class: 'bg-risk-low' },
  { label: 'Medium (5-9)', class: 'bg-risk-medium' },
  { label: 'High (10-14)', class: 'bg-risk-high' },
  { label: 'Critical (15-25)', class: 'bg-risk-critical' }
]

const getCellRating = (rowIndex, colIndex) => {
  const impact = 5 - rowIndex
  const likelihood = colIndex + 1
  return impact * likelihood
}

const getCellClass = (rowIndex, colIndex) => {
  const rating = getCellRating(rowIndex, colIndex)
  const count = props.matrix[rowIndex][colIndex]

  let bgClass = ''
  if (rating >= 1 && rating <= 4) bgClass = 'bg-risk-low'
  else if (rating >= 5 && rating <= 9) bgClass = 'bg-risk-medium'
  else if (rating >= 10 && rating <= 14) bgClass = 'bg-risk-high'
  else if (rating >= 15) bgClass = 'bg-risk-critical'

  // Add animation if there are risks in this cell
  const animation = count > 0 && rating >= 15 ? 'animate-pulse-red shadow-red-glow' : ''

  return `${bgClass} ${animation} ${count > 0 ? 'opacity-100' : 'opacity-40'}`
}

const getCellTitle = (rowIndex, colIndex, count) => {
  const impact = 5 - rowIndex
  const likelihood = colIndex + 1
  const rating = impact * likelihood
  return `Likelihood: ${likelihood}, Impact: ${impact}\nRating: ${rating}\nRisks: ${count}`
}

const onCellClick = (rowIndex, colIndex) => {
  if (props.risksByCell && props.risksByCell[rowIndex] && props.risksByCell[rowIndex][colIndex]) {
    const risks = props.risksByCell[rowIndex][colIndex]
    emit('cell-click', { rowIndex, colIndex, risks })
  }
}
</script>

<style scoped>
.writing-mode-vertical {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  transform: rotate(180deg);
}
</style>
