import axios from "axios"

const apiBaseURL = import.meta.env.VITE_API_BASE_URL
  || (import.meta.env.DEV ? "http://127.0.0.1:8000" : undefined)

const api = axios.create({
  baseURL: apiBaseURL,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
