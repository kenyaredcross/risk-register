import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/main.css'
import axios from 'axios'

// Configure axios globally BEFORE any components load
function getCsrfToken() {
  // Frappe exposes the CSRF token as window.frappe.csrf_token
  return window.frappe?.csrf_token || ''
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
