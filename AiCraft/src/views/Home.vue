<template>
  <section
    class="container mx-auto pt-8 text-gray-800 dark:text-gray-200">
    <h1 class="text-4xl font-bold">
      Hi, I'm Vivek 👋
    </h1>

    <p class="mt-3 text-xl text-gray-600 dark:text-gray-400">
      Learning and building Machine Learning, Deep Learning & Generative AI
    </p>

    <p class="mt-6 leading-relaxed text-gray-600 dark:text-gray-400">
      This website showcases my hands-on experience, projects, and continuous
      learning in ML, DL, and GenAI using tools like PyTorch, LangChain,
      and modern LLM-based systems.
    </p>

    <div class="mt-10 flex gap-4">
      <router-link
        to="/projects"
        class="px-5 py-2 rounded-md bg-emerald-500
               text-white font-medium
               hover:bg-emerald-600 transition"
      >
        View Projects
      </router-link>

      <router-link
        to="/about"
        class="px-5 py-2 rounded-md border
               border-emerald-500 text-emerald-500
               hover:bg-emerald-50 dark:hover:bg-gray-800
               transition"
      >
        About Me
      </router-link>
    </div>
  </section>
</template>

<script setup>
</script>


<style scoped>

</style>
