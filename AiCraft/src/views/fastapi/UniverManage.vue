<script setup>
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"

import StudentTab from "../../components/university-management/StudentTab.vue"
import InstructorTab from "../../components/university-management/InstructorTab.vue"
import CourseTab from "../../components/university-management/CourseTab.vue"
import DepartmentTab from "../../components/university-management/DepartmentTab.vue"
import EmptyState from "../../components/university-management/EmptyState.vue"
const route = useRoute()
const router = useRouter()

const tabs = [
  { key: "students", label: "Students", component: StudentTab },
  { key: "instructors", label: "Instructors", component: InstructorTab },
  { key: "courses", label: "Courses", component: CourseTab },
  { key: "departments", label: "Departments", component: DepartmentTab },
]

const activeTab = computed(() => route.query.tab || "")

const activeComponent = computed(() => {
  return tabs.find(t => t.key === activeTab.value)?.component || EmptyState
})

const selectTab = (key) => {
  router.replace({
    query: {tab: key }
  })
}
</script>

<template>
  <section class="container mx-auto pt-8 text-gray-800 dark:text-gray-200">
    <h1 class="text-3xl font-bold mb-2">University Management</h1>

    <p class="mb-8 text-gray-600 dark:text-gray-400">
      This section describes a University Management system built using FastAPI,
      focusing on clean API design, scalability, and real-world academic workflows.
    </p>

    <!-- Tabs -->
    <div class="flex gap-6 mb-6 border-b border-gray-200 dark:border-gray-700">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="selectTab(tab.key)"
        class="pb-2 text-sm font-medium border-b-2 transition"
        :class="activeTab === tab.key
          ? 'border-blue-600 text-blue-600'
          : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-blue-600'"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab Content -->
    <main
      class="rounded-lg border p-6
             border-gray-200 dark:border-gray-700
             bg-white dark:bg-gray-900"
    >
      <component :is="activeComponent" />
    </main>
  </section>
</template>
