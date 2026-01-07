<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Course Management</h2>

    <!-- Search Inputs -->
    <div class="flex gap-4 flex-col sm:flex-row mb-6">
      <input
        v-model="title"
        type="text"
        placeholder="Search by course title"
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
        @click="searchCourses"
        class="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white"
      >
        Search
      </button>
    </div>

    <!-- Results -->
    <div v-if="courses.length" class="overflow-x-auto">
      <table class="min-w-full border border-gray-300 dark:border-gray-700">
        <thead class="bg-gray-100 dark:bg-gray-800">
          <tr>
            <th class="p-2 text-left">Course ID</th>
            <th class="p-2 text-left">Title</th>
            <th class="p-2 text-left">Department</th>
            <th class="p-2 text-left">Credits</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="course in courses"
            :key="course.course_id"
            class="border-t border-gray-300 dark:border-gray-700"
          >
            <td class="p-2">{{ course.course_id }}</td>
            <td class="p-2">{{ course.title }}</td>
            <td class="p-2">{{ course.dept_name }}</td>
            <td class="p-2">{{ course.credits }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="text-gray-500">No courses found.</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppConfigStore } from "../../stores/appConfig"

const configStore = useAppConfigStore()

const route = useRoute()
const router = useRouter()

const title = ref(route.query.title || '')
const department = ref(route.query.department || '')
const courses = ref([])

/**
 * Fetch courses
 */
const fetchCourses = async () => {
  if (route.query.tab !== 'courses') return

  if (!title.value && !department.value) {
    courses.value = []
    return
  }

  const params = new URLSearchParams()
  if (title.value) params.append('title', title.value)
  if (department.value) params.append('department', department.value)

  const response = await fetch(`${configStore.baseUniverManageApiUrl}/courses?${params.toString()}`)

  if (!response.ok) {
    courses.value = []
    return
  }

  courses.value = await response.json()
}

/**
 * Update URL query (preserve tab)
 */
const searchCourses = () => {
  router.push({
    query: {
      ...route.query,
      title: title.value || undefined,
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
    title.value = q.title || ''
    department.value = q.department || ''
    await fetchCourses()
  },
  { immediate: true }
)
</script>
