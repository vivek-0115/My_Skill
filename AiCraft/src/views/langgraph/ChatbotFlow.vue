<template>
    <div class="flex flex-row h-full">

        <aside class="w-64 h- border-r border-gray-200 dark:border-gray-700 flex flex-col">

            <div class="px-2 py-2">
                <h1 class="text-lg font-semibold">ChatGraph</h1>
            </div>

            <div class="py-2 px-1 border-b border-gray-200 dark:border-gray-700">
                <button @click="createNewChat" class="rounded-lg hover:bg-zinc-700 flex w-full px-2 py-2">
                    + New Chat
                </button>
            </div>

            <div class="flex-1 overflow-y-auto space-y-1 py-2 px-2">
                <div v-for="chat in recentChats" :key="chat.id" @click="selectChat(chat)"
                    class="px-2 py-2 rounded-lg cursor-pointer hover:bg-zinc-800"
                    :class="chat.id === activeChatId ? 'bg-zinc-800' : ''">
                    <p class="text-sm truncate">{{ chat.title }}</p>
                </div>
            </div>
        </aside>

        <!-- Main Chat Area -->
        <main class="flex-1 flex flex-row">

            <aside class="w-52 border-r border-gray-200 dark:border-gray-700 p-4">
                <h3 class="text-sm font-semibold mb-4">Models</h3>

                <div class="space-y-2">
                    <div v-for="(group, index) in modelGroups" :key="index" class="rounded-lg">
                        <!-- Parent Model -->
                        <button @click="toggleGroup(group.name)"
                            class="w-full flex items-center justify-between px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
                            <span>{{ group.name }}</span>
                            <span>{{ openGroup === group.name ? '▾' : '▸' }}</span>
                        </button>

                        <!-- Child Models -->
                        <div v-if="openGroup === group.name" class="ml-4 mt-1 space-y-1">
                            <button v-for="model in group.models" :key="model" @click="selectModel(model)" class="w-full text-left px-3 py-1.5 rounded-md text-sm
                 hover:bg-blue-100 dark:hover:bg-blue-900" :class="activeModel === model
                    ? 'bg-blue-600 text-white'
                    : ''">
                                {{ model }}
                            </button>
                        </div>
                    </div>
                </div>

                <div class="mt-6 text-xs text-gray-500">
                    Active model:
                    <span class="text-blue-600 font-medium">
                        {{ activeModel || 'None' }}
                    </span>
                </div>
            </aside>

            <section class="flex-1 flex flex-col">

                <!-- Header -->
                <header class="border-b border-gray-200 dark:border-gray-700 px-6 py-3">
                    <h2 class="text-sm text-zinc-400">
                        {{ activeChatTitle }}
                    </h2>
                </header>

                <!-- Chat Messages -->
                <div class="flex-1 overflow-y-auto px-16 py-4 space-y-4">
                    <div v-for="(msg, index) in chat" :key="index" class="flex"
                        :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
                        <div class="max-w-[75%] px-4 py-2 rounded-xl whitespace-pre-wrap" :class="msg.role === 'user'
                            ? 'bg-blue-600 text-white rounded-br-sm'
                            : hasError && msg.content.includes('Failed')
                                ? 'bg-red-200 text-red-800 rounded-bl-sm'
                                : 'bg-gray-200 text-gray-800 rounded-bl-sm'">
                            <ChatLoading v-if="msg.content === ''" />
                            <span v-else>{{ msg.content }}</span>
                        </div>
                    </div>
                    <div ref="bottomRef"></div>
                </div>

                <div class="pb-6 pt-4 flex justify-center">
                    <form @submit.prevent="sendMessage" class="relative">
                        <!-- Input -->
                        <input v-model="message" type="text" placeholder="Send a message..." class="w-150 bg-gray-200 h-12 pl-5 pr-14
                                         outline-none text-gray-700 text-lg rounded-full" />

                        <button type="submit" :disabled="!message.trim()" class="absolute right-2 top-1/2 -translate-y-1/2
                                 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-full
                                   w-9 h-9 flex items-center justify-center">
                            <PaperAirplaneIcon class="w-4 h-4" />
                        </button>
                    </form>
                </div>

            </section>

        </main>

    </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from "vue"
import { useRoute, useRouter } from "vue-router"
import { PaperAirplaneIcon } from "@heroicons/vue/24/solid"
import { useAppConfigStore } from "../../stores/appConfig"
import ChatLoading from "../../components/ChatLoading.vue"

const configStore = useAppConfigStore()
const route = useRoute()
const router = useRouter()

const message = ref("")
const chat = ref([])
const recentChats = ref([])
const activeChatId = ref('')
const activeChatTitle = ref("Weather in Patna")
const hasError = ref(false)

const bottomRef = ref(null)
const chatContainer = ref(null)

const modelGroups = [
    {
        name: "Gemini",
        models: ["gemini-1.5-pro", "gemini-2.0-flash"]
    },
    {
        name: "OpenAI",
        models: ["gpt-4o", "gpt-4-turbo"]
    },
    {
        name: "HuggingFace",
        models: ["Mistral-7B-Instruct-v0.2", "Llama-3.1-8B-Instruct", "gpt-oss-120b", "Qwen3-4B-Instruct-2507", "Kimi-K2-Instruct-0905"]
    }
]

const openGroup = ref(null)
const activeModel = ref("gemini-2.0-flash")

const toggleGroup = (groupName) => {
    openGroup.value = openGroup.value === groupName ? null : groupName
}

const selectModel = (model) => {
    activeModel.value = model
}

const createNewChat = async () => {
    try {
        const res = await fetch(`${configStore.chatbotFlow}/new-chat`)
        const result = await res.json()

        if (!result.success) {
            throw new Error("Failed to create new chat")
        }

        const newChat = {
            id: result.tid,
            title: result.title
        }

        recentChats.value.unshift(newChat)

        activeChatId.value = newChat.id
        activeChatTitle.value = newChat.title

        chat.value = []

        router.push({
            query: { tid: newChat.id }
        })

    } catch (err) {
        console.error("New chat error:", err)
    }
}


const selectChat = async (chatItem) => {
    activeChatId.value = chatItem.id
    activeChatTitle.value = chatItem.title

    router.push({
        query: {
            tid: chatItem.id
        }
    })

    await getChatMessages(chatItem.id)
}

const getChatMessages = async (chatId) => {
    try {
        const res = await fetch(
            `${configStore.chatbotFlow}/chats?tid=${chatId}`
        )
        const result = await res.json()

        if (!result.success) {
            throw new Error("Failed to load chat messages")
        }

        chat.value = result.data.messages
    } catch (err) {
        chat.value = []
        console.error(err)
    }
}


const getRecentChats = async () => {
    try {
        const res = await fetch(`${configStore.chatbotFlow}/recent-chats`)
        const result = await res.json()

        if (!result.success) {
            throw new Error("Failed to fetch recent chats")
        }

        recentChats.value = result.data

        // Auto-open latest chat
        if (recentChats.value.length > 0) {
            const latestChat = recentChats.value[0]

            activeChatId.value = latestChat.id
            activeChatTitle.value = latestChat.title

            router.replace({
                query: {
                    tid: latestChat.id
                }
            })

            await getChatMessages(latestChat.id)
        }

    } catch (err) {
        error.value = "Failed to load recent chats"
        console.error(err)
    }
}

onMounted(async () => {
    await getRecentChats()

    const tidFromUrl = route.query.tid
    if (tidFromUrl) {
        const chatItem = recentChats.value.find(c => c.id === tidFromUrl)
        if (chatItem) {
            activeChatId.value = chatItem.id
            activeChatTitle.value = chatItem.title
            await getChatMessages(chatItem.id)
        }
    }
})

const startStreaming = (result, assistantIndex) => {
    try {
        const { request_id } = result

        const es = new EventSource(
            `${configStore.chatbotFlow}/chat/stream?request_id=${request_id}`
        )

        console.log("in sse.")

        es.addEventListener("token", (e) => {
            chat.value[assistantIndex].content += e.data
            console.log("hii")
        })

        es.addEventListener("token", (e) => {
            chat.value[assistantIndex].content += e.data
            scrollToBottom()
        })


        es.addEventListener("done", (e) => {
            console.log(e.data)
            es.close()
        })

        es.onerror = () => {
            chat.value[assistantIndex].content = "Streaming error"
            es.close()
        }

    } catch (err) {
        console.error("SSE error:", err)
    }
}

const sendMessage = async () => {
    if (!message.value.trim()) return

    hasError.value = false

    chat.value.push({
        role: "user",
        content: message.value
    })

    const userInput = message.value
    message.value = ""

    chat.value.push({ role: "assistant", content: "" })
    const assistantIndex = chat.value.length - 1

    try {
        const res = await fetch(`${configStore.chatbotFlow}/chat/message`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tid: activeChatId.value, query: userInput })
        })

        const result = await res.json()

        if (!result.success) {
            throw new Error(result.message || "Sending message failed.")
        }
        console.log(result)
        startStreaming(result, assistantIndex)

    } catch (err) {
        hasError.value = true
        chat.value[assistantIndex].content = "Failed to get response from server."
        console.error(err)

    }
}

</script>
