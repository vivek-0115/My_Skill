<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Department Management</h2>

    <!-- Search Inputs -->
    <div class="flex gap-4 flex-col sm:flex-row mb-6">
      <input
        v-model="deptName"
        type="text"
        placeholder="Search by department name"
        class="flex-1 p-2 rounded-md border
               border-gray-300 dark:border-gray-700
               bg-white dark:bg-gray-800
               focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        v-model="building"
        type="text"
        placeholder="Search by building"
        class="flex-1 p-2 rounded-md border
               border-gray-300 dark:border-gray-700
               bg-white dark:bg-gray-800
               focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <button
        @click="searchDepartments"
        class="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white"
      >
        Search
      </button>
    </div>

    <!-- Results -->
    <div v-if="departments.length" class="overflow-x-auto">
      <table class="min-w-full border border-gray-300 dark:border-gray-700">
        <thead class="bg-gray-100 dark:bg-gray-800">
          <tr>
            <th class="p-2 text-left">Department</th>
            <th class="p-2 text-left">Building</th>
            <th class="p-2 text-left">Budget</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="dept in departments"
            :key="dept.dept_name"
            class="border-t border-gray-300 dark:border-gray-700"
          >
            <td class="p-2">{{ dept.dept_name }}</td>
            <td class="p-2">{{ dept.building }}</td>
            <td class="p-2">{{ dept.budget }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="text-gray-500">No departments found.</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppConfigStore } from "../../stores/appConfig"

const configStore = useAppConfigStore()

const route = useRoute()
const router = useRouter()

const deptName = ref(route.query.dept_name || '')
const building = ref(route.query.building || '')
const departments = ref([])

/**
 * Fetch departments
 */
const fetchDepartments = async () => {
  if (route.query.tab !== 'departments') return

  if (!deptName.value && !building.value) {
    departments.value = []
    return
  }

  const params = new URLSearchParams()
  if (deptName.value) params.append('dept_name', deptName.value)
  if (building.value) params.append('building', building.value)

  const response = await fetch(`${configStore.baseUniverManageApiUrl}/departments?${params.toString()}`)

  if (!response.ok) {
    departments.value = []
    return
  }

  departments.value = await response.json()
}

/**
 * Update URL query (preserve tab)
 */
const searchDepartments = () => {
  router.push({
    query: {
      ...route.query,
      dept_name: deptName.value || undefined,
      building: building.value || undefined
    }
  })
}

/**
 * Watch URL changes
 */
watch(
  () => route.query,
  async (q) => {
    deptName.value = q.dept_name || ''
    building.value = q.building || ''
    await fetchDepartments()
  },
  { immediate: true }
)
</script>

