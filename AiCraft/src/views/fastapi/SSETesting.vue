<template>
  <section class="container mx-auto py-8 text-gray-800 dark:text-gray-200">

    <h1 class="text-3xl font-bold mb-2">SSE Test Console</h1>

    <p class="mb-10 text-gray-600 dark:text-gray-400">
      Send any text and watch the FastAPI backend stream processing steps in real time using Server-Sent Events.
    </p>

    <div
      class="rounded-lg border p-6
             border-gray-200 dark:border-gray-700
             bg-white dark:bg-gray-900"
    >
      <label class="block mb-2 font-semibold text-gray-700 dark:text-gray-300">
        Input Text
      </label>

      <textarea
        v-model="feedback"
        rows="5"
        placeholder="Type any text here..."
        class="w-full p-3 rounded-md
               border border-gray-300 dark:border-gray-700
               bg-white dark:bg-gray-800
               focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <button
        @click="startSSE"
        :disabled="loading || !feedback"
        class="mt-4 px-6 py-2 rounded-md
               bg-blue-600 hover:bg-blue-700
               text-white font-medium
               disabled:opacity-50"
      >
        {{ loading ? "Streaming..." : "Start SSE" }}
      </button>

      <p v-if="error" class="mt-4 text-red-500">
        {{ error }}
      </p>
    </div>

    <div v-if="events.length" class="mt-10">
      <div
        class="rounded-lg border p-6
               border-gray-200 dark:border-gray-700
               bg-white dark:bg-gray-900"
      >
        <h2 class="text-xl font-semibold mb-4">Live SSE Stream</h2>

        <ul class="space-y-2 font-mono text-sm">
          <li v-for="(msg, i) in events" :key="i">
            {{ msg }}
          </li>
        </ul>
      </div>
    </div>

  </section>
</template>
<script setup>
import { ref, onBeforeUnmount } from "vue"
import { useAppConfigStore } from "../../stores/appConfig"

const configStore = useAppConfigStore()

const feedback = ref("")
const loading = ref(false)
const error = ref("")
const events = ref([])

let evtSource = null

onBeforeUnmount(() => {
  if (evtSource) evtSource.close()
})

const startSSE = async () => {
  if (!feedback.value.trim()) return

  loading.value = true
  error.value = ""
  events.value = []

  try {
    // 1️⃣ Send text
    const res = await fetch(`${configStore.baseUrl}/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: feedback.value }),
    })

    if (!res.ok) throw new Error("Failed to start process")

    const { process_id } = await res.json()

    // 2️⃣ Open SSE stream
    evtSource = new EventSource(
      `${configStore.baseUrl}/process/${process_id}`
    )

    evtSource.onmessage = (e) => {
      events.value.push(e.data)
    }

    evtSource.addEventListener("done", () => {
      events.value.push("✔ Processing complete")
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
