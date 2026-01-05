<template>
  <button
    @click="toggleTheme"
    class="px-3 py-1 rounded-md border text-sm
           border-gray-300 dark:border-gray-600
           text-gray-700 dark:text-gray-200
           hover:bg-gray-200 dark:hover:bg-gray-700
           transition outline-transparent"
  >
    <span v-if="isDark">🌟 Dark</span>
    <span v-else>☀️ Light</span>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)

function applyTheme() {
  const html = document.documentElement
  if (isDark.value) {
    html.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    html.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

function toggleTheme() {
  isDark.value = !isDark.value
  applyTheme()
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    applyTheme()
  }
})
</script>
