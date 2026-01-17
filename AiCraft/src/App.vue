<template>
  <section class="bg-white dark:bg-gray-900">
    <!-- Navbar -->
    <header class="border-b border-gray-200 dark:border-gray-700 h-[7vh]">
      <div class="container mx-auto flex items-center justify-between">
        <!-- Brand -->
        <router-link to="/" class="flex items-center gap-3 group">
          <!-- Logo -->
          <img src=".././public/2728.svg" alt="AiCraft Logo" class="h-9 w-9 group-hover:scale-105 transition" />

          <!-- Name -->
          <span class="text-2xl font-bold tracking-tight dark:text-orange-400 text-orange-500">
            AiCraft
          </span>
        </router-link>

        <!-- Navigation -->
        <nav class="flex items-center gap-8">
          <!-- Links -->
          <div class="hidden md:flex items-center gap-6 text-gray-700 dark:text-gray-200 font-medium">
            <router-link to="/" class="nav-link">Home</router-link>
            <router-link to="/ml-projects" class="nav-link">ML Projects</router-link>
            <router-link to="/dl-projects" class="nav-link">DL Projects</router-link>
            <router-link to="/langchain" class="nav-link">LangChain</router-link>
            <router-link to="/langgraph" class="nav-link">LangGraph</router-link>
            <router-link to="/fastapi" class="nav-link">FastAPI</router-link>
            <router-link to="/projects" class="nav-link">Projects</router-link>
            <router-link to="/about" class="nav-link">About</router-link>
          </div>

          <!-- Right Action -->
          <ThemeToggle />
        </nav>
      </div>
    </header>

    <!-- Page Content -->
    <main class="h-[93vh]">
      <router-view />
    </main>
  </section>
</template>

<script setup>
import ThemeToggle from "./components/ThemeToggle.vue"
</script>
