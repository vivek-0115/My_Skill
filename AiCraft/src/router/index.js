import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import MLProjects from '../views/MLProjects.vue'
import DLProjects from '../views/DLProjects.vue'
import LangChain from '../views/LangChain.vue'
import Prompt from '../views/langchain/Prompt.vue'
import FeedbackResponse from '../views/langchain/FeedbackResponse.vue'
import Rag from '../views/langchain/Rag.vue'
import Projects from '../views/Projects.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/ml-projects', name: 'MLProjects', component: MLProjects },
  { path: '/dl-projects', name: 'DLProjects', component: DLProjects },
  { path: '/langchain', name: 'LangChain', component: LangChain },
  { path: '/langchain/prompt', name: 'Prompt', component: Prompt },
  { path: '/langchain/feedback-response-generator', name: 'FeedbackResponse', component: FeedbackResponse },
  { path: '/langchain/rag', name: 'Rag', component: Rag },
  { path: '/projects', name: 'Projects', component: Projects },
  { path: '/about', name: 'About', component: About }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
