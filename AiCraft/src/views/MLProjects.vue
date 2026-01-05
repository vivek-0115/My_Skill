<template>
    <section class="container mx-auto pt-8 text-gray-800 dark:text-gray-200">
        <h1 class="text-3xl font-bold">Machine Learning Projects</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
            Practical implementations of classical machine learning algorithms.
        </p>

        <div class="mt-10 grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- LEFT -->
            <ProjectList :projects="projects" :active="activeProject" @select="activeProject = $event" />

            <!-- RIGHT -->
            <div class="md:col-span-2 border rounded-lg p-6
               border-gray-200 dark:border-gray-700
               bg-white dark:bg-gray-900">
                <component :is="activeComponent" />
            </div>
        </div>
    </section>
</template>

<script setup>
import { computed, ref } from 'vue'

import ProjectList from '../components/ml-projects/ProjectList.vue'
import ProjectEmpty from '../components/ml-projects/ProjectEmpty.vue'
import ProjectRecommender from '../components/ml-projects/RecommenderSystem.vue'
import ProjectHouseRent from '../components/ml-projects/HouseRentPrediction.vue'

const activeProject = ref(null)

const projects = [
    { id: 'recommender', name: 'Recommender System' },
    { id: 'house-rent', name: 'House Rent Predictor' },
]

const componentMap = {
    'recommender': ProjectRecommender,
    'house-rent': ProjectHouseRent,
}

const activeComponent = computed(() => {
    return activeProject.value
        ? componentMap[activeProject.value]
        : ProjectEmpty
})
</script>
