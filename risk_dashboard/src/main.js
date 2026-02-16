import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/main.css'
import axios from 'axios'

// Configure axios globally BEFORE any components load
// Frappe injects: <script>frappe.csrf_token = "...";</script> replacing <!-- csrf_token -->
// When unauthenticated the token is the string "None" — treat that as absent.
const INVALID_TOKENS = new Set(['', 'None', 'fetch', '{{ csrf_token }}', undefined, null])

function getCsrfToken() {
  // 1. Prefer the server-injected token on window.frappe (set by Frappe's template replacement)
  const injected = window.frappe && window.frappe.csrf_token
  if (!INVALID_TOKENS.has(injected)) return injected

  // 2. Fallback: read from csrf_token cookie (present when logged in)
  const match = document.cookie.split('; ').find(row => row.startsWith('csrf_token='))
  const cookie = match ? decodeURIComponent(match.split('=')[1]) : null
  if (cookie && !INVALID_TOKENS.has(cookie)) return cookie

  // 3. Last resort: tell Frappe to fetch a new token
  return 'fetch'
}

axios.defaults.baseURL = window.location.origin
axios.defaults.withCredentials = true
axios.defaults.headers.common['X-Frappe-CSRF-Token'] = getCsrfToken()

// Refresh CSRF header before every mutating request
axios.interceptors.request.use(config => {
  if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
    config.headers['X-Frappe-CSRF-Token'] = getCsrfToken()
  }
  config.withCredentials = true
  return config
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
