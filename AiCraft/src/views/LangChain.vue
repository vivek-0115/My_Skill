<template>
  <section class="container mx-auto pt-8 text-gray-800 dark:text-gray-200">
    <h1 class="text-3xl font-bold mb-2">LangChain</h1>

    <p class="mb-10 text-gray-600 dark:text-gray-400">
      Practical implementations of LangChain concepts with real examples.
    </p>

    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <router-link
        v-for="topic in topics"
        :key="topic.slug"
        :to="`/langchain/${topic.slug}`"
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
    title: 'Prompt Templates',
    slug: 'prompt',
    desc: 'Creating reusable and dynamic prompts using LangChain.'
  },
  {
    title: 'Chains',
    slug: 'chains',
    desc: 'Combining multiple LLM calls into structured workflows.'
  },
  {
    title: 'Retrieval Augmented Generation (RAG)',
    slug: 'rag',
    desc: 'Enhancing LLM responses using external knowledge sources.'
  }
]
</script>
