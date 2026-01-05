<template>
  <section class="">
    <div class="border-b border-gray-200 dark:border-gray-700">
      <nav class="flex items-center  justify-between py-6 container mx-auto">
        <!-- Left -->
        <div class="flex gap-4 text-gray-700 dark:text-gray-200 font-medium text-lg">
          <router-link class="nav-link" to="/">Home</router-link>
          <router-link class="nav-link" to="/ml-projects">ML Projects</router-link>
          <router-link class="nav-link" to="/dl-projects">DL Projects</router-link>
          <router-link class="nav-link" to="/langchain">LangChain</router-link>
          <router-link class="nav-link" to="/projects">Projects</router-link>
          <router-link class="nav-link" to="/about">About</router-link>
        </div>

        <!-- Right -->
        <ThemeToggle />
      </nav>
    </div>

    <router-view />
  </section>
</template>

<script setup>
import ThemeToggle from './components/ThemeToggle.vue'
import router from './router';
</script>

<style scoped></style>
