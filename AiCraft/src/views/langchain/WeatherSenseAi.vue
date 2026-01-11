<template>
  <section class="container mx-auto py-8 text-gray-800 dark:text-gray-200">
    <h1 class="text-2xl font-bold">WeatherSense AI</h1>
    <p class="mt-2 mb-6 text-gray-600 dark:text-gray-400">
      An AI agent combining real-time weather APIs and web search to deliver accurate forecasts, alerts, and contextual
      insights.
    </p>

    <!-- Input Card -->
    <div class="bg-white dark:bg-gray-900 border dark:border-gray-700 rounded-xl p-6 shadow-sm">
      <label class="block text-xl font-medium mb-4">
        Ask weather-related questions.
      </label>

      <textarea v-model="query" rows="3" placeholder="e.g. Is there any cyclone warning in Odisha?" class="w-full rounded-lg border dark:border-gray-700
               bg-white dark:bg-gray-800 p-3
               focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>

      <button @click="askAgent" :disabled="loading || !query" class="mt-4 w-full py-2 rounded-lg
               bg-blue-600 text-white font-medium
               hover:bg-blue-700 disabled:opacity-50">
        {{ loading ? update : 'Ask WeatherSense AI' }}
      </button>
    </div>

    <!-- Tool Hint -->
    <div class="mt-4 text-sm text-gray-500 dark:text-gray-400 text-center">
      Uses <span class="font-medium">Weather APIs</span> for forecasts and
      <span class="font-medium">Web Search</span> for alerts & advisories
    </div>

    <!-- Response -->
    <div v-if="response" class="mt-10">
      <h2 class="text-lg font-semibold mb-3">Response</h2>
      <div class="p-5 rounded-lg border dark:border-gray-700
                  bg-gray-50 dark:bg-gray-800
                  text-gray-700 dark:text-gray-300 whitespace-pre-line">
        {{ response }}
        <p v-if="error" class="mt-4 text-red-500">
          {{ error }}
        </p>
      </div>
    </div>

    <!-- Example Queries -->
    <div class="mt-14">
      <h2 class="text-lg font-semibold mb-4">Try asking</h2>
      <div class="grid md:grid-cols-2 gap-4 text-sm">
        <button v-for="example in examples" :key="example" @click="query = example" class="p-4 rounded-lg border dark:border-gray-700
                 hover:bg-gray-50 dark:hover:bg-gray-800 text-left">
          {{ example }}
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import { useAppConfigStore } from "../../stores/appConfig"

const query = ref('')
const update = ref("")
const response = ref("")
const loading = ref(false)
const error = ref("")
const configStore = useAppConfigStore()

let evtSource = null

onBeforeUnmount(() => {
  if (evtSource) evtSource.close()
})

const examples = [
  "What's the weather in Mumbai tomorrow?",
  "Is there any cyclone warning in Odisha?",
  "Why is it unusually cold in Bangalore today?",
  "Is it safe to travel given today's weather?"
]

const askAgent = async () => {
  loading.value = true
  response.value = ""
  update.value = "Thinking..."
  error.value = ""

  const url = `${configStore.weatherSenseAi}`

  try {
    const res = await fetch(`${url}/start-stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query.value }),
    })

    if (!res.ok) throw new Error("Failed to start process")

    const { process_id } = await res.json()

    //Open SSE stream
    evtSource = new EventSource(`${url}/stream/${process_id}`)

    evtSource.onmessage = (e) => {
      let data = JSON.parse(e.data)
      update.value = data.message

      if (data.content) {
        response.value = data.content
      }
    }

    evtSource.addEventListener("done", () => {
      loading.value = false
      evtSource.close()
    })

    evtSource.addEventListener("error", (e) => {
      response.value = e.data
      loading.value = false
      evtSource.close()
    })

    evtSource.onerror = () => {
      error.value = "SSE connection lost"
      loading.value = false
      evtSource.close()
    }

  } catch (err) {
    console.error(err)
    error.value = "Failed to start SSE process"
    loading.value = false
  }
}

</script>
