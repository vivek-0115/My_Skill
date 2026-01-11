import { defineStore } from "pinia"
import { ref } from "vue"

export const useAppConfigStore = defineStore("appConfig", () => {
  // Base API URL (single source of truth)
  const baseUrl = ref("http://127.0.0.1:8000")
  const baseApiUrl = ref(`${baseUrl.value}/api`)
  const baseUniverManageApiUrl = ref(`${baseApiUrl.value}/university-management`)
  const weatherSenseAi = ref(`${baseApiUrl.value}/weatherSense-ai`)

  return {
    baseUrl,
    baseApiUrl,
    baseUniverManageApiUrl,
    weatherSenseAi,
  }
})

