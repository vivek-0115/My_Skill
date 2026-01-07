<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Student Management</h2>

    <!-- Search Inputs -->
    <div class="flex gap-4 flex-col sm:flex-row mb-6">
      <input
        v-model="name"
        type="text"
        placeholder="Search by student name"
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
        @click="searchStudents"
        class="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white"
      >
        Search
      </button>
    </div>

    <!-- Results -->
    <div v-if="students.length" class="overflow-x-auto">
      <table class="min-w-full border border-gray-300 dark:border-gray-700">
        <thead class="bg-gray-100 dark:bg-gray-800">
          <tr>
            <th class="p-2 text-left">ID</th>
            <th class="p-2 text-left">Name</th>
            <th class="p-2 text-left">Department</th>
            <th class="p-2 text-left">Total Credits</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="student in students"
            :key="student.id"
            class="border-t border-gray-300 dark:border-gray-700"
          >
            <td class="p-2">{{ student.id }}</td>
            <td class="p-2">{{ student.name }}</td>
            <td class="p-2">{{ student.dept_name }}</td>
            <td class="p-2">{{ student.tot_cred }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="text-gray-500">No students found.</p>
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
const students = ref([])

/**
 * Fetch students using native fetch
 */
const fetchStudents = async () => {
  if (route.query.tab !== 'students') return

  if (!name.value && !department.value) {
    students.value = []
    return
  }

  const params = new URLSearchParams()

  if (name.value) params.append('name', name.value)
  if (department.value) params.append('department', department.value)

  const response = await fetch(`${configStore.baseUniverManageApiUrl}/students?${params.toString()}`)

  if (!response.ok) {
    students.value = []
    return
  }

  students.value = await response.json()
}

/**
 * Update URL query (preserve tab)
 */
const searchStudents = () => {
  router.push({
    query: {
      ...route.query, // keep tab + other params
      name: name.value || undefined,
      department: department.value || undefined
    }
  })
}

/**
 * React to URL changes safely
 */
watch(
  () => route.query,
  async (newQuery) => {
    name.value = newQuery.name || ''
    department.value = newQuery.department || ''

    await fetchStudents()
  },
  { immediate: true }
)
</script>

