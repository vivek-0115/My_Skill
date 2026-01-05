<template>
  <aside
    class="border rounded-lg border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 h-full">
    <ul>
      <li
        v-for="project in projects"
        :key="project.id"
        @click="$emit('select', project.id)"
        class="px-4 py-3 cursor-pointer border-b last:border-b-0
               border-gray-200 dark:border-gray-700
               hover:bg-gray-100 dark:hover:bg-gray-800"
        :class="{
          'bg-emerald-50 dark:bg-gray-800 font-medium':
            active === project.id
        }"
      >
        {{ project.name }}
      </li>
    </ul>
  </aside>
</template>

<script setup>
defineProps({
  projects: Array,
  active: String
})
</script>
