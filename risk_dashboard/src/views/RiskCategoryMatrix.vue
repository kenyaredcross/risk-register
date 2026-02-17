<template>
  <div class="animate-fade-in">
    <!-- Page Header -->
    <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
      <div>
        <h1 class="text-3xl font-bold text-charcoal mb-1">Risk Category Matrix</h1>
        <p class="text-medium-gray">Risk distribution by category across {{ viewBy === 'unit' ? 'units' : viewBy === 'project' ? 'projects' : 'departments' }}</p>
      </div>
      <!-- Controls: view toggle + transpose -->
      <div class="flex items-center gap-2 self-start flex-wrap">
        <!-- View toggle -->
        <div class="inline-flex items-center bg-light-gray rounded-lg p-1 border border-light-border">
          <button
            v-if="isGlobalUser"
            type="button"
            @click="viewBy = 'department'"
            :class="viewBy === 'department' ? 'bg-white shadow text-charcoal' : 'text-medium-gray hover:text-charcoal'"
            class="px-4 py-1.5 rounded-md transition-all text-sm font-medium"
          >
            By Department
          </button>
          <button
            type="button"
            @click="viewBy = 'unit'"
            :class="viewBy === 'unit' ? 'bg-white shadow text-charcoal' : 'text-medium-gray hover:text-charcoal'"
            class="px-4 py-1.5 rounded-md transition-all text-sm font-medium"
          >
            By Unit
          </button>
          <button
            type="button"
            @click="viewBy = 'project'"
            :class="viewBy === 'project' ? 'bg-white shadow text-charcoal' : 'text-medium-gray hover:text-charcoal'"
            class="px-4 py-1.5 rounded-md transition-all text-sm font-medium"
          >
            By Project
          </button>
        </div>
        <!-- Transpose toggle -->
        <button
          type="button"
          @click="transposed = !transposed"
          :class="transposed ? 'bg-charcoal text-white border-charcoal' : 'bg-white text-charcoal border-light-border hover:border-charcoal'"
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-sm font-medium transition-all"
          title="Transpose: swap rows and columns"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4" />
          </svg>
          Transpose
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Department filter (only shown in unit/dept view, and for global users or when not locked) -->
        <div v-if="viewBy !== 'project' && (isGlobalUser || viewBy === 'unit' || !departmentLocked)">
          <label class="block text-sm font-medium text-charcoal mb-1">
            Department
            <span v-if="departmentLocked" class="text-xs text-medium-gray font-normal ml-1">(your department)</span>
          </label>
          <select v-model="filterDepartment" class="input" :disabled="departmentLocked">
            <option value="">All Departments</option>
            <option v-for="dept in departments" :key="dept.name" :value="dept.name">
              {{ dept.department_name }}
            </option>
          </select>
        </div>
        <!-- Status filter -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-1">Status</label>
          <select v-model="filterStatus" class="input">
            <option value="">All Statuses</option>
            <option value="Open">Open</option>
            <option value="In Progress">In Progress</option>
            <option value="Pending Approval">Pending Approval</option>
            <option value="Closed">Closed</option>
            <option value="Mitigated">Mitigated</option>
          </select>
        </div>
        <!-- Risk level filter -->
        <div>
          <label class="block text-sm font-medium text-charcoal mb-1">Risk Level</label>
          <select v-model="filterLevel" class="input">
            <option value="">All Levels</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-2 sm:grid-cols-5 gap-4 mb-6">
      <!-- Total — clears level filter -->
      <div
        class="card text-center py-4 cursor-pointer transition-all duration-150 select-none"
        :class="filterLevel === '' ? 'ring-2 ring-charcoal ring-offset-2' : 'hover:scale-[1.02]'"
        @click="filterLevel = ''"
        title="Show all levels"
      >
        <div class="text-3xl font-bold text-charcoal">{{ matrixData.total || 0 }}</div>
        <div class="text-sm text-medium-gray mt-1">Total Risks</div>
      </div>
      <!-- Per-level cards -->
      <div
        v-for="level in ['Critical','High','Medium','Low']"
        :key="level"
        class="card text-center py-4 cursor-pointer transition-all duration-150 select-none"
        :class="filterLevel === level ? ringClass(level) : 'hover:scale-[1.02]'"
        @click="filterLevel = filterLevel === level ? '' : level"
        :title="`Filter by ${level}`"
      >
        <div class="text-3xl font-bold" :class="levelTextClass(level)">{{ levelCount(level) }}</div>
        <div class="text-sm mt-1" :class="levelTextClass(level)">{{ level }}</div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-primary"></div>
    </div>

    <template v-else>
      <!-- Matrix Table -->
      <div v-if="matrixData.axis && matrixData.axis.length > 0" class="card overflow-hidden mb-6">
        <div class="overflow-x-auto">

          <!-- Normal orientation: rows = categories, columns = axis items -->
          <table v-if="!transposed" class="w-full border-collapse text-xs">
            <thead>
              <tr class="bg-light-gray">
                <th class="px-3 py-2 text-left text-xs font-semibold text-charcoal uppercase sticky left-0 bg-light-gray z-10 border-r border-light-border min-w-[130px] max-w-[160px]">
                  Category
                </th>
                <th
                  v-for="col in matrixData.axis"
                  :key="col.name"
                  class="py-2 px-1 text-center text-xs font-semibold text-charcoal border-r border-light-border w-14"
                >
                  <div class="truncate max-w-[56px] mx-auto leading-tight" :title="col.label">{{ col.label }}</div>
                  <div class="text-xs font-normal text-medium-gray mt-0.5">({{ matrixData.totals_by_axis[col.name] || 0 }})</div>
                </th>
                <th class="py-2 px-2 text-center text-xs font-semibold text-charcoal w-10">Total</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="cat in matrixData.categories"
                :key="cat"
                class="border-t border-light-border hover:bg-off-white transition-colors"
              >
                <td class="px-3 py-2 text-xs font-medium text-charcoal sticky left-0 bg-white z-10 border-r border-light-border leading-tight">
                  {{ cat }}
                </td>
                <td
                  v-for="col in matrixData.axis"
                  :key="col.name"
                  class="py-1.5 px-1 text-center border-r border-light-border"
                >
                  <button
                    v-if="cellData(cat, col.name).count > 0"
                    @click="openCell(cat, col)"
                    class="inline-flex items-center justify-center w-8 h-8 rounded-lg font-bold text-sm transition-all duration-200 hover:scale-110 cursor-pointer shadow-sm"
                    :class="cellBgClass(cellData(cat, col.name).highest_level)"
                    :title="`${cat} / ${col.label}: ${cellData(cat, col.name).count} risk(s)`"
                  >
                    {{ cellData(cat, col.name).count }}
                  </button>
                  <span v-else class="text-light-border text-base opacity-40">—</span>
                </td>
                <td class="py-1.5 px-2 text-center font-semibold text-charcoal text-xs">
                  {{ matrixData.totals_by_category[cat] || 0 }}
                </td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="border-t-2 border-light-border bg-light-gray">
                <td class="px-3 py-2 font-semibold text-charcoal text-xs sticky left-0 bg-light-gray z-10 border-r border-light-border">Total</td>
                <td
                  v-for="col in matrixData.axis"
                  :key="col.name"
                  class="py-2 px-1 text-center font-semibold text-charcoal text-xs border-r border-light-border"
                >
                  {{ matrixData.totals_by_axis[col.name] || 0 }}
                </td>
                <td class="py-2 px-2 text-center font-bold text-charcoal text-xs">{{ matrixData.total || 0 }}</td>
              </tr>
            </tfoot>
          </table>

          <!-- Transposed orientation: rows = axis items, columns = categories -->
          <table v-else class="w-full border-collapse text-xs">
            <thead>
              <tr class="bg-light-gray">
                <th class="px-3 py-2 text-left text-xs font-semibold text-charcoal uppercase sticky left-0 bg-light-gray z-10 border-r border-light-border min-w-[130px] max-w-[160px]">
                  {{ viewBy === 'unit' ? 'Unit' : viewBy === 'project' ? 'Project' : 'Department' }}
                </th>
                <th
                  v-for="cat in matrixData.categories"
                  :key="cat"
                  class="py-2 px-1 text-center text-xs font-semibold text-charcoal border-r border-light-border w-14"
                >
                  <div class="truncate max-w-[56px] mx-auto leading-tight" :title="cat">{{ cat }}</div>
                  <div class="text-xs font-normal text-medium-gray mt-0.5">({{ matrixData.totals_by_category[cat] || 0 }})</div>
                </th>
                <th class="py-2 px-2 text-center text-xs font-semibold text-charcoal w-10">Total</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="col in matrixData.axis"
                :key="col.name"
                class="border-t border-light-border hover:bg-off-white transition-colors"
              >
                <td class="px-3 py-2 text-xs font-medium text-charcoal sticky left-0 bg-white z-10 border-r border-light-border leading-tight">
                  <div class="truncate max-w-[150px]" :title="col.label">{{ col.label }}</div>
                </td>
                <td
                  v-for="cat in matrixData.categories"
                  :key="cat"
                  class="py-1.5 px-1 text-center border-r border-light-border"
                >
                  <button
                    v-if="cellData(cat, col.name).count > 0"
                    @click="openCell(cat, col)"
                    class="inline-flex items-center justify-center w-8 h-8 rounded-lg font-bold text-sm transition-all duration-200 hover:scale-110 cursor-pointer shadow-sm"
                    :class="cellBgClass(cellData(cat, col.name).highest_level)"
                    :title="`${cat} / ${col.label}: ${cellData(cat, col.name).count} risk(s)`"
                  >
                    {{ cellData(cat, col.name).count }}
                  </button>
                  <span v-else class="text-light-border text-base opacity-40">—</span>
                </td>
                <td class="py-1.5 px-2 text-center font-semibold text-charcoal text-xs">
                  {{ matrixData.totals_by_axis[col.name] || 0 }}
                </td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="border-t-2 border-light-border bg-light-gray">
                <td class="px-3 py-2 font-semibold text-charcoal text-xs sticky left-0 bg-light-gray z-10 border-r border-light-border">Total</td>
                <td
                  v-for="cat in matrixData.categories"
                  :key="cat"
                  class="py-2 px-1 text-center font-semibold text-charcoal text-xs border-r border-light-border"
                >
                  {{ matrixData.totals_by_category[cat] || 0 }}
                </td>
                <td class="py-2 px-2 text-center font-bold text-charcoal text-xs">{{ matrixData.total || 0 }}</td>
              </tr>
            </tfoot>
          </table>

        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="card text-center py-16">
        <svg class="w-16 h-16 text-medium-gray mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-medium-gray">No data available for the selected filters</p>
      </div>

      <!-- Legend -->
      <div class="flex items-center flex-wrap gap-4 mt-2 px-1">
        <span class="text-xs text-medium-gray font-medium">Legend:</span>
        <span v-for="level in ['Critical','High','Medium','Low']" :key="level" class="flex items-center gap-1.5">
          <span class="w-5 h-5 rounded text-xs font-bold text-white flex items-center justify-center" :class="cellBgClass(level)">n</span>
          <span class="text-xs text-medium-gray">{{ level }}</span>
        </span>
        <span class="flex items-center gap-1.5">
          <span class="text-medium-gray text-lg leading-none opacity-40">—</span>
          <span class="text-xs text-medium-gray">No risks</span>
        </span>
      </div>
    </template>

    <!-- Cell Detail Modal -->
    <div
      v-if="selectedCell"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="selectedCell = null"
    >
      <div class="bg-white rounded-xl shadow-elegant-xl max-w-lg w-full max-h-[80vh] flex flex-col">
        <!-- Modal header -->
        <div class="px-6 py-4 border-b border-light-border flex items-center justify-between">
          <div>
            <h3 class="text-lg font-bold text-charcoal">{{ selectedCell.category }}</h3>
            <p class="text-sm text-medium-gray">{{ selectedCell.axisLabel }}</p>
          </div>
          <button @click="selectedCell = null" class="p-2 hover:bg-light-gray rounded-lg transition-colors">
            <svg class="w-5 h-5 text-medium-gray" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <!-- Modal body -->
        <div class="overflow-y-auto flex-1 px-6 py-4">
          <p class="text-sm text-medium-gray mb-4">{{ selectedCell.risks.length }} risk(s) in this cell</p>
          <div class="space-y-3">
            <div
              v-for="risk in selectedCell.risks"
              :key="risk.name"
              class="flex items-center justify-between p-3 rounded-lg border border-light-border hover:border-charcoal transition-colors cursor-pointer"
              @click="goToRisk(risk.name)"
            >
              <div>
                <div class="text-sm font-medium text-charcoal">{{ risk.name }}</div>
                <div class="text-xs text-medium-gray mt-0.5">{{ risk.status }}</div>
              </div>
              <span
                class="px-2 py-0.5 rounded-full text-xs font-semibold whitespace-nowrap"
                :class="levelBadgeClass(risk.risk_level)"
              >
                {{ risk.risk_level }}
              </span>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-light-border">
          <button @click="selectedCell = null" class="btn btn-outline w-full">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '../composables/useApi'
import axios from 'axios'

const router = useRouter()
const api = useApi()

const loading = ref(false)
const isGlobalUser = ref(true)   // updated after getCurrentUser resolves
const viewBy = ref('department') // may change to 'unit' for non-global users
const transposed = ref(true)
const filterDepartment = ref('')
const filterStatus = ref('')
const filterLevel = ref('')
const departmentLocked = ref(false)
const departments = ref([])
const matrixData = ref({ categories: [], axis: [], matrix: {}, totals_by_category: {}, totals_by_axis: {}, total: 0 })
const selectedCell = ref(null)

// ── Helpers ──────────────────────────────────────────────────────────────────

const cellData = (cat, axisName) => {
  return matrixData.value.matrix?.[cat]?.[axisName] || { count: 0, highest_level: null, risks: [] }
}

const levelCount = (level) => {
  let count = 0
  const matrix = matrixData.value.matrix || {}
  for (const cat of Object.values(matrix)) {
    for (const cell of Object.values(cat)) {
      count += cell.risks.filter(r => r.risk_level === level).length
    }
  }
  return count
}

const cellBgClass = (level) => {
  switch (level) {
    case 'Critical': return 'bg-risk-critical text-white opacity-100'
    case 'High':     return 'bg-risk-high text-white opacity-100'
    case 'Medium':   return 'bg-risk-medium text-white opacity-100'
    case 'Low':      return 'bg-risk-low text-white opacity-100'
    default:         return 'bg-gray-200 text-gray-500'
  }
}

const levelTextClass = (level) => {
  switch (level) {
    case 'Critical': return 'text-red-600'
    case 'High':     return 'text-orange-600'
    case 'Medium':   return 'text-yellow-600'
    case 'Low':      return 'text-green-600'
    default:         return 'text-charcoal'
  }
}

const ringClass = (level) => {
  switch (level) {
    case 'Critical': return 'ring-2 ring-red-500 ring-offset-2'
    case 'High':     return 'ring-2 ring-orange-500 ring-offset-2'
    case 'Medium':   return 'ring-2 ring-yellow-500 ring-offset-2'
    case 'Low':      return 'ring-2 ring-green-500 ring-offset-2'
    default:         return 'ring-2 ring-charcoal ring-offset-2'
  }
}

const levelBadgeClass = (level) => {
  switch (level) {
    case 'Critical': return 'bg-red-100 text-red-700'
    case 'High':     return 'bg-orange-100 text-orange-700'
    case 'Medium':   return 'bg-yellow-100 text-yellow-700'
    case 'Low':      return 'bg-green-100 text-green-700'
    default:         return 'bg-gray-100 text-gray-600'
  }
}

const openCell = (cat, col) => {
  const data = cellData(cat, col.name)
  if (data.count === 0) return
  selectedCell.value = { category: cat, axisName: col.name, axisLabel: col.label, risks: data.risks }
}

const goToRisk = (name) => {
  selectedCell.value = null
  router.push(`/risk/${name}`)
}

// ── Data loading ─────────────────────────────────────────────────────────────

const loadMatrix = async () => {
  loading.value = true
  matrixData.value = await api.getCategoryMatrix({
    viewBy: viewBy.value,
    filterDepartment: filterDepartment.value,
    filterStatus: filterStatus.value,
    filterLevel: filterLevel.value,
  })
  loading.value = false
}

const loadDepts = async () => {
  try {
    const res = await axios.get('/api/method/krcs_risk.krcs_risk_management.doctype.program_risk_register.api.get_departments')
    departments.value = res.data.message || []
  } catch (e) {
    console.error(e)
  }
}

// Reload whenever filters or viewBy change
watch([viewBy, filterDepartment, filterStatus, filterLevel], loadMatrix)

onMounted(async () => {
  await loadDepts()
  // Determine user scope and set view defaults
  try {
    const user = await api.getCurrentUser()
    if (!user.is_global_viewer) {
      isGlobalUser.value = false
      // HOD/PM/staff: default to "By Unit", lock department filter
      viewBy.value = 'unit'
      if (user.department) {
        filterDepartment.value = user.department
        departmentLocked.value = true
      }
    }
  } catch (e) {
    console.error(e)
  }
  await loadMatrix()
})
</script>
