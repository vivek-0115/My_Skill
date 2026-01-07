<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Instructor Management</h2>

    <!-- Search Inputs -->
    <div class="flex gap-4 flex-col sm:flex-row mb-6">
      <input
        v-model="name"
        type="text"
        placeholder="Search by instructor name"
        class="flex-1 p-2 rounded-md border
               border-gray-300 dark:border-gray-700
               bg-white dark:bg-gray-800
               focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        v-model="department"
        type="text"
        placeholder="Search by department"
        class="flex-1 p-2 rounded-md border
               border-gray-300 dark:border-gray-700
               bg-white dark:bg-gray-800
               focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <button
        @click="searchInstructors"
        class="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white"
      >
        Search
      </button>
    </div>

    <!-- Results -->
    <div v-if="instructors.length" class="overflow-x-auto">
      <table class="min-w-full border border-gray-300 dark:border-gray-700">
        <thead class="bg-gray-100 dark:bg-gray-800">
          <tr>
            <th class="p-2 text-left">ID</th>
            <th class="p-2 text-left">Name</th>
            <th class="p-2 text-left">Department</th>
            <th class="p-2 text-left">Salary</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="inst in instructors"
            :key="inst.id"
            class="border-t border-gray-300 dark:border-gray-700"
          >
            <td class="p-2">{{ inst.id }}</td>
            <td class="p-2">{{ inst.name }}</td>
            <td class="p-2">{{ inst.dept_name }}</td>
            <td class="p-2">{{ inst.salary }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="text-gray-500">No instructors found.</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppConfigStore } from "../../stores/appConfig"

const configStore = useAppConfigStore()

const route = useRoute()
const router = useRouter()

const name = ref(route.query.name || '')
const department = ref(route.query.department || '')
const instructors = ref([])

/**
 * Fetch instructors
 */
const fetchInstructors = async () => {
  if (route.query.tab !== 'instructors') return

  if (!name.value && !department.value) {
    instructors.value = []
    return
  }

  const params = new URLSearchParams()
  if (name.value) params.append('name', name.value)
  if (department.value) params.append('department', department.value)

  const response = await fetch(`${configStore.baseUniverManageApiUrl}/instructors?${params.toString()}`)

  if (!response.ok) {
    instructors.value = []
    return
  }

  instructors.value = await response.json()
}

/**
 * Update URL query (preserve tab)
 */
const searchInstructors = () => {
  router.push({
    query: {
      ...route.query,
      name: name.value || undefined,
      department: department.value || undefined
    }
  })
}

/**
 * Watch URL changes
 */
watch(
  () => route.query,
  async (q) => {
    name.value = q.name || ''
    department.value = q.department || ''
    await fetchInstructors()
  },
  { immediate: true }
)
</script>

