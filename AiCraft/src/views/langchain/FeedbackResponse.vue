<script setup>
import { ref, computed } from "vue"
import { marked } from "marked"
import { useAppConfigStore } from "../../stores/appConfig"

const configStore = useAppConfigStore()

const feedback = ref("")
const loading = ref(false)
const sentiment = ref("")
const response = ref("")
const error = ref("")

const renderedResponse = computed(() =>
  response.value ? marked.parse(response.value) : ""
)

const generateResponse = async () => {
  if (!feedback.value.trim()) return

  loading.value = true
  sentiment.value = ""
  response.value = ""
  error.value = ""

  try {
    const res = await fetch(`${configStore.baseApiUrl}/feedback-response-generator`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        feedback: feedback.value,
      }),
    })

    if (!res.ok) {
      throw new Error("Failed to generate response")
    }

    const data = await res.json()
    sentiment.value = data.sentiment
    response.value = data.response
  } catch (err) {
    error.value = "Something went wrong while processing the feedback."
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="container mx-auto py-8 text-gray-800 dark:text-gray-200">

    <!-- Header -->
    <h1 class="text-3xl font-bold mb-2">Feedback Response Generator</h1>

    <p class="mb-10 text-gray-600 dark:text-gray-400">
      This section demonstrates how AI analyzes user feedback, detects its
      sentiment, and generates an appropriate response based on that sentiment.
    </p>

    <!-- Feedback Form -->
    <div
      class="rounded-lg border p-6
             border-gray-200 dark:border-gray-700
             bg-white dark:bg-gray-900"
    >
      <label class="block mb-2 font-semibold text-gray-700 dark:text-gray-300">
        Enter User Feedback
      </label>

      <textarea
        v-model="feedback"
        rows="5"
        placeholder="Paste user feedback here..."
        class="w-full p-3 rounded-md
               border border-gray-300 dark:border-gray-700
               bg-white dark:bg-gray-800
               focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <button
        @click="generateResponse"
        :disabled="loading || !feedback"
        class="mt-4 px-6 py-2 rounded-md
               bg-blue-600 hover:bg-blue-700
               text-white font-medium
               disabled:opacity-50"
      >
        {{ loading ? "Generating..." : "Generate Response" }}
      </button>

      <!-- Error -->
      <p v-if="error" class="mt-4 text-red-500">
        {{ error }}
      </p>
    </div>

    <!-- Result -->
    <div v-if="response" class="mt-10">

      <!-- Sentiment -->
      <div class="mb-4">
        <span class="font-semibold">Detected Sentiment:</span>
        <span
          class="ml-2 px-3 py-1 rounded-full text-sm font-medium"
          :class="{
            'bg-green-100 text-green-700': sentiment === 'positive',
            'bg-red-100 text-red-700': sentiment === 'negative',
            'bg-gray-100 text-gray-700': sentiment !== 'positive' && sentiment !== 'negative'
          }"
        >
          {{ sentiment }}
        </span>
      </div>

      <!-- AI Response -->
      <div
        class="rounded-lg border p-6
               border-gray-200 dark:border-gray-700
               bg-white dark:bg-gray-900"
      >
        <h2 class="text-xl font-semibold mb-4">Generated Response</h2>

        <div
          v-html="renderedResponse"
          class="prose dark:prose-invert max-w-none"
        ></div>
      </div>

    </div>
  </section>
</template>

