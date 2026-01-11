<template>
  <section class="container mx-auto pt-8 text-gray-800 dark:text-gray-200">
    <h1 class="text-3xl font-bold mb-2">LangChain</h1>

    <p class="mb-10 text-gray-600 dark:text-gray-400">
      Practical implementations of LangChain concepts with real examples.
    </p>

    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <router-link v-for="topic in topics" :key="topic.slug" :to="`/langchain/${topic.slug}`" class="p-6 rounded-lg border
               border-gray-200 dark:border-gray-700
               bg-white dark:bg-gray-900
               hover:shadow-lg transition">
        <h3 class="text-lg font-semibold mb-2">
          {{ topic.title }}
        </h3>

        <p class="text-sm text-gray-600 dark:text-gray-400">
          {{ topic.desc }}
        </p>

        <span class="inline-block mt-4 text-xs font-medium text-emerald-600 dark:text-emerald-400">
          {{ topic.tech }}
        </span>
      </router-link>
    </div>
  </section>
</template>

<script setup>
const topics = [
  {
    title: 'Prompt Templates',
    slug: 'prompt',
    desc: 'Creating reusable and dynamic prompts using LangChain.',
    tech: 'LangChain · Prompt Templates · LLM'
  },
  {
    title: 'Feedback Response Generator',
    slug: 'feedback-response-generator',
    desc: 'Generates clear, constructive, and context-aware responses to user feedback.',
    tech: 'LangChain · Runnables · Chains · LLM'
  },
  {
    title: 'WeatherSense AI',
    slug: 'weatherSense-ai',
    desc: 'AI agent combining weather APIs and web search for forecasts and alerts.',
    tech: 'LangChain · Tool Calling · Weather API · Web Search · LLM'
  }
]
</script>
