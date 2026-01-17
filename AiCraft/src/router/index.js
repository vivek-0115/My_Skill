import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import MLProjects from '../views/MLProjects.vue'
import DLProjects from '../views/DLProjects.vue'
import LangChain from '../views/LangChain.vue'
import LangGraph from '../views/LangGraph.vue'
import Prompt from '../views/langchain/Prompt.vue'
import FeedbackResponse from '../views/langchain/FeedbackResponse.vue'
import WeatherSense from '../views/langchain/WeatherSenseAi.vue'
import FastAPI from '../views/FastAPI.vue'
import UniverManage from '../views/fastapi/UniverManage.vue'
import SSETesting from '../views/fastapi/SSETesting.vue'
import ChatbotFlow from '../views/langgraph/ChatbotFlow.vue'
import Projects from '../views/Projects.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/ml-projects', name: 'MLProjects', component: MLProjects },
  { path: '/dl-projects', name: 'DLProjects', component: DLProjects },
  { path: '/langchain', name: 'LangChain', component: LangChain },
  { path: '/langgraph', name: 'LangGraph', component: LangGraph },
  { path: '/langchain/prompt', name: 'Prompt', component: Prompt },
  { path: '/langchain/feedback-response-generator', name: 'FeedbackResponse', component: FeedbackResponse },
  { path: '/langchain/weatherSense-ai', name: 'WeatherSense', component: WeatherSense },
  { path: '/fastapi', name: 'FastAPI', component: FastAPI },
  { path: '/fastapi/university-management', name: 'UniverManage', component: UniverManage },
  { path: '/fastapi/sse-testing', name: 'SSETesting', component: SSETesting },
  { path: '/langgraph/chatbot-flow', name: 'ChatbotFlow', component: ChatbotFlow },
  { path: '/projects', name: 'Projects', component: Projects },
  { path: '/about', name: 'About', component: About }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
