<template>
  <section
    class="container mx-auto pt-8 text-gray-800 dark:text-gray-200">
    <h1 class="text-3xl font-bold">Projects</h1>

    <p class="mt-2 text-gray-600 dark:text-gray-400">
      A collection of hands-on projects and experiments.
    </p>

    <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="project in projects"
        :key="project.title"
        class="p-6 rounded-lg border
               border-gray-200 dark:border-gray-700
               bg-white dark:bg-gray-900
               hover:shadow-lg transition"
      >
        <h3 class="text-lg font-semibold">
          {{ project.title }}
        </h3>

        <p class="mt-3 text-sm text-gray-600 dark:text-gray-400">
          {{ project.desc }}
        </p>

        <span
          class="inline-block mt-4 text-xs font-medium
                 text-emerald-600 dark:text-emerald-400"
        >
          {{ project.tech }}
        </span>
      </div>
    </div>
  </section>
</template>

<script setup>
const projects = [
  {
    title: 'Sentiment Analysis with BiLSTM',
    desc: 'Built a sentiment classifier using PyTorch and BiLSTM architecture.',
    tech: 'PyTorch · NLP'
  },
  {
    title: 'GenAI Chatbot',
    desc: 'LLM-powered chatbot using LangChain and prompt engineering.',
    tech: 'LangChain · LLMs'
  },
  {
    title: 'ML Dashboard',
    desc: 'Interactive Vue dashboard to visualize ML model results.',
    tech: 'Vue · Chart.js'
  }
]
</script>
