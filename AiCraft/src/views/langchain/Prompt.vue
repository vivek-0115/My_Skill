<script setup>
import { ref, computed } from "vue"
import { marked } from "marked"

// UI state
const paper = ref("")
const style = ref("")
const length = ref("")
const format = ref("")
const focus = ref("")
const difficulty = ref("")

const result = ref("")
const loading = ref(false)

const renderedMarkdown = computed(() =>
    result.value ? marked.parse(result.value) : ""
)

const summarize = async () => {
    // basic validation
    if (!paper.value || !style.value || !length.value) return

    loading.value = true
    result.value = ""

    try {
        const res = await fetch("http://127.0.0.1:8000/prompt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                paper: paper.value,
                style: style.value,
                length: length.value,
                format: format.value,
                focus: focus.value,
                difficulty: difficulty.value,
            }),
        })

        const data = await res.json()
        result.value = data.response
    } catch (err) {
        result.value = "Error while calling API"
        console.error(err)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <section class="container mx-auto py-8 text-gray-800 dark:text-gray-200">
        <h1 class="text-2xl font-bold">
            Prompt Templates
        </h1>

        <p class="text-gray-600 dark:text-gray-400 mb-6 mt-2">
            This page demonstrates how to use LangChain prompt templates
            to create reusable and dynamic prompts.
        </p>

        <div class="rounded-lg border p-6
             border-gray-200 dark:border-gray-700
             bg-white dark:bg-gray-900">
            <h2 class="font-semibold text-3xl mb-4">Research Assistant</h2>

            <!-- Input -->

            <main class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">

                <!-- Research Paper -->
                <div>
                    <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                        Research Paper
                    </label>
                    <select v-model="paper" class="w-full rounded-md border
             border-gray-300 dark:border-gray-700
             bg-white dark:bg-gray-800
             px-3 py-2
             focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option disabled value="">Select a research paper</option>
                        <option>Attention Is All You Need (Transformer)</option>
                        <option>BERT: Pre-training of Deep Bidirectional Transformers</option>
                        <option>GPT Series (GPT-1 to GPT-4)</option>
                        <option>ResNet: Deep Residual Learning</option>
                        <option>AlexNet</option>
                        <option>YOLO: Real-Time Object Detection</option>
                        <option>Diffusion Models</option>
                        <option>Custom / Upload Your Own</option>
                    </select>
                    <p class="mt-1 text-xs text-gray-500">
                        Choose the paper you want to understand
                    </p>
                </div>

                <!-- Explanation Style -->
                <div>
                    <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                        Explanation Style
                    </label>
                    <select v-model="style" class="w-full rounded-md border
             border-gray-300 dark:border-gray-700
             bg-white dark:bg-gray-800
             px-3 py-2
             focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option disabled value="">Select explanation style</option>
                        <option>Beginner Friendly (Intuitive & Simple)</option>
                        <option>Intermediate (Concept + Examples)</option>
                        <option>Technical (Implementation Focused)</option>
                        <option>Core-Oriented (Key Ideas Only)</option>
                        <option>Mathematical (Equations & Proofs)</option>
                        <option>Researcher Perspective (Assumptions & Limits)</option>
                    </select>
                    <p class="mt-1 text-xs text-gray-500">
                        Tailor the explanation to your learning level
                    </p>
                </div>

                <!-- Explanation Length -->
                <div>
                    <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                        Explanation Depth
                    </label>
                    <select v-model="length" class="w-full rounded-md border
             border-gray-300 dark:border-gray-700
             bg-white dark:bg-gray-800
             px-3 py-2
             focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option disabled value="">Select depth</option>
                        <option>Very Short (Key idea only)</option>
                        <option>Short (1–2 paragraphs)</option>
                        <option>Medium (3–5 paragraphs)</option>
                        <option>Long (Detailed explanation)</option>
                        <option>Very Long (Section-wise breakdown)</option>
                    </select>
                    <p class="mt-1 text-xs text-gray-500">
                        Control how detailed the response should be
                    </p>
                </div>

                <!-- Output Format -->
                <div>
                    <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                        Output Format
                    </label>
                    <select v-model="format" class="w-full rounded-md border
             border-gray-300 dark:border-gray-700
             bg-white dark:bg-gray-800
             px-3 py-2
             focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option disabled value="">Select format</option>
                        <option>Plain Explanation</option>
                        <option>Bullet Points</option>
                        <option>Step-by-Step</option>
                        <option>With Pseudocode</option>
                        <option>With Diagrams Description</option>
                        <option>Interview-Ready Notes</option>
                    </select>
                    <p class="mt-1 text-xs text-gray-500">
                        Choose how the explanation should be structured
                    </p>
                </div>

                <!-- Focus Area -->
                <div>
                    <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                        Focus Area
                    </label>
                    <select v-model="focus" class="w-full rounded-md border
             border-gray-300 dark:border-gray-700
             bg-white dark:bg-gray-800
             px-3 py-2
             focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option disabled value="">Select focus</option>
                        <option>High-Level Intuition</option>
                        <option>Architecture & Components</option>
                        <option>Training Procedure</option>
                        <option>Loss Functions</option>
                        <option>Advantages & Limitations</option>
                        <option>Real-World Applications</option>
                        <option>Comparison with Other Papers</option>
                    </select>
                    <p class="mt-1 text-xs text-gray-500">
                        Emphasize specific aspects of the paper
                    </p>
                </div>

                <!-- Difficulty Level -->
                <div>
                    <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                        Difficulty Level
                    </label>
                    <select v-model="difficulty" class="w-full rounded-md border
             border-gray-300 dark:border-gray-700
             bg-white dark:bg-gray-800
             px-3 py-2
             focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option disabled value="">Select difficulty</option>
                        <option>Easy</option>
                        <option>Moderate</option>
                        <option>Hard</option>
                        <option>Research-Level</option>
                    </select>
                    <p class="mt-1 text-xs text-gray-500">
                        Adjust conceptual difficulty
                    </p>
                </div>

            </main>



            <!-- Button -->
            <button @click="summarize" :disabled="loading || !paper || !style || !length" class="mt-4 px-6 py-2 rounded-md
         bg-blue-600 hover:bg-blue-700
         disabled:opacity-50 text-white">
                {{ loading ? "Summarizing..." : "Summarize" }}
            </button>


            <!-- Result -->
            <div v-if="result" class="mt-6 mb-2">
                <h3 class="text-xl underline font-semibold mb-3">Result:</h3>

                <div v-html="renderedMarkdown" class="prose dark:prose-invert max-w-none"></div>
            </div>
        </div>
    </section>
</template>
