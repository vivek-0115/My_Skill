<template>
  <section class="container mx-auto pt-8 text-gray-800 dark:text-gray-200">
    <h1 class="text-3xl font-bold mb-2">FastAPI</h1>

    <p class="mb-10 text-gray-600 dark:text-gray-400">
      Practical FastAPI projects and patterns for building modern, high-performance APIs.
    </p>

    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <router-link
        v-for="topic in topics"
        :key="topic.slug"
        :to="`/fastapi/${topic.slug}`"
        class="p-6 rounded-lg border
               border-gray-200 dark:border-gray-700
               bg-white dark:bg-gray-900
               hover:shadow-lg transition"
      >
        <h3 class="text-lg font-semibold mb-2">
          {{ topic.title }}
        </h3>

        <p class="text-sm text-gray-600 dark:text-gray-400">
          {{ topic.desc }}
        </p>
      </router-link>
    </div>
  </section>
</template>

<script setup>
const topics = [
  {
    title: 'University Management API',
    slug: 'university-management',
    desc: 'Designing REST APIs for students, courses, instructors, and enrollments using FastAPI.'
  },
  {
    title: "Server-Sent Events Tester",
    slug: "sse-testing",
    desc: "A debugging page for validating SSE streams, progress updates, and connection behavior."
  },
]
</script>
