<template>
  <div id="app" class="min-h-screen bg-off-white">
    <!-- Header — hidden on login page -->
    <header v-if="!isLoginPage" class="bg-white shadow-elegant sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <!-- Logo & Title -->
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 bg-red-primary rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-charcoal">KRCS Risk Management</h1>
              <p class="text-sm text-medium-gray">Kenya Red Cross Society</p>
            </div>
          </div>

          <!-- Navigation -->
          <div class="hidden md:flex items-center space-x-6">
            <nav class="flex space-x-6">
              <!-- Dashboard dropdown -->
              <div class="relative" ref="dashboardDropdownRef">
                <button
                  type="button"
                  class="nav-link flex items-center gap-1"
                  :class="{ 'nav-link-active': isDashboardActive }"
                  @click="dashboardDropdownOpen = !dashboardDropdownOpen"
                >
                  Dashboard
                  <svg class="w-3.5 h-3.5 mt-0.5 transition-transform" :class="{ 'rotate-180': dashboardDropdownOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <!-- Dropdown panel -->
                <div
                  v-if="dashboardDropdownOpen"
                  class="absolute left-0 top-full mt-1 w-48 bg-white rounded-lg shadow-elegant border border-light-border py-1 z-50"
                >
                  <button
                    @click="switchDashboard('/dashboard')"
                    class="w-full text-left px-4 py-2.5 text-sm hover:bg-light-gray transition-colors flex items-center justify-between"
                    :class="$route.path === '/dashboard' ? 'text-red-primary font-semibold' : 'text-charcoal'"
                  >
                    Risk Dashboard
                    <svg v-if="$route.path === '/dashboard'" class="w-3.5 h-3.5 text-red-primary" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </button>
                  <button
                    @click="switchDashboard('/matrix')"
                    class="w-full text-left px-4 py-2.5 text-sm hover:bg-light-gray transition-colors flex items-center justify-between"
                    :class="$route.path === '/matrix' ? 'text-red-primary font-semibold' : 'text-charcoal'"
                  >
                    Category Matrix
                    <svg v-if="$route.path === '/matrix'" class="w-3.5 h-3.5 text-red-primary" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
              <router-link
                to="/risks"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/risks' }"
              >
                Risk Register
              </router-link>
              <router-link
                to="/coi-dashboard"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path.startsWith('/coi') }"
              >
                COI Declarations
              </router-link>
              <!-- System Manager → full Admin (starts at Departments) -->
              <router-link
                v-if="authStore.isSystemManager"
                to="/admin/departments"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path.startsWith('/admin') }"
              >
                Admin
              </router-link>
              <!-- HOD → Admin (Departments & Units for their dept) -->
              <router-link
                v-else-if="authStore.isHOD"
                to="/admin/departments"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path.startsWith('/admin') }"
              >
                Admin
              </router-link>
              <!-- PM only → Users page -->
              <router-link
                v-else-if="authStore.isPM"
                to="/admin/users"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/admin/users' }"
              >
                Users
              </router-link>
            </nav>

            <!-- Add Risk Button -->
            <router-link
              to="/risk/create"
              class="flex items-center space-x-1 bg-red-primary hover:bg-red-dark text-white px-4 py-2 rounded-lg transition-colors duration-200 font-medium shadow-sm hover:shadow-md"
              title="Add New Risk"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              <span>Add Risk</span>
            </router-link>

            <!-- User + Logout -->
            <div class="flex items-center space-x-3 pl-4 border-l border-light-border">
              <div class="text-right hidden lg:block">
                <div class="text-sm font-medium text-charcoal leading-tight">{{ authStore.fullName || authStore.user }}</div>
                <div class="text-xs text-medium-gray">{{ authStore.user }}</div>
              </div>
              <router-link to="/profile" title="My Profile" class="w-8 h-8 rounded-full bg-charcoal text-white flex items-center justify-center text-sm font-bold uppercase hover:bg-red-primary transition-colors">
                {{ (authStore.fullName || authStore.user || '?')[0] }}
              </router-link>
              <button @click="handleLogout" title="Sign Out" class="p-2 text-medium-gray hover:text-red-primary hover:bg-light-gray rounded-lg transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Mobile menu button -->
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2 rounded-lg hover:bg-light-gray">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        <!-- Mobile menu -->
        <div v-if="mobileMenuOpen" class="md:hidden py-4 border-t border-light-border space-y-2">
          <div class="flex items-center space-x-3 pb-3 border-b border-light-border mb-2">
            <div class="w-8 h-8 rounded-full bg-charcoal text-white flex items-center justify-center text-sm font-bold uppercase">
              {{ (authStore.fullName || authStore.user || '?')[0] }}
            </div>
            <div>
              <div class="text-sm font-medium text-charcoal">{{ authStore.fullName || authStore.user }}</div>
              <div class="text-xs text-medium-gray">{{ authStore.user }}</div>
            </div>
          </div>
          <div class="py-1">
            <p class="text-xs font-semibold text-medium-gray uppercase tracking-wide mb-1">Dashboards</p>
            <router-link to="/dashboard" class="block py-1.5 pl-3 text-charcoal hover:text-red-primary" :class="{ 'text-red-primary font-semibold': $route.path === '/dashboard' }" @click="mobileMenuOpen = false">
              Risk Dashboard
            </router-link>
            <router-link to="/matrix" class="block py-1.5 pl-3 text-charcoal hover:text-red-primary" :class="{ 'text-red-primary font-semibold': $route.path === '/matrix' }" @click="mobileMenuOpen = false">
              Category Matrix
            </router-link>
          </div>
          <router-link to="/risks" class="block py-2 text-charcoal hover:text-red-primary" @click="mobileMenuOpen = false">
            Risk Register
          </router-link>
          <router-link v-if="authStore.isSystemManager || authStore.isHOD" to="/admin/departments" class="block py-2 text-charcoal hover:text-red-primary" @click="mobileMenuOpen = false">
            Admin
          </router-link>
          <router-link v-else-if="authStore.isPM" to="/admin/users" class="block py-2 text-charcoal hover:text-red-primary" @click="mobileMenuOpen = false">
            Users
          </router-link>
          <router-link
            to="/risk/create"
            class="flex items-center space-x-2 bg-red-primary hover:bg-red-dark text-white px-4 py-2 rounded-lg transition-colors duration-200 font-medium mt-2"
            @click="mobileMenuOpen = false"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>Add Risk</span>
          </router-link>
          <router-link to="/profile" class="flex items-center space-x-2 w-full py-2 text-charcoal hover:text-red-primary" @click="mobileMenuOpen = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span>My Profile</span>
          </router-link>
          <button @click="handleLogout" class="flex items-center space-x-2 w-full py-2 text-medium-gray hover:text-red-primary">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer — hidden on login page -->
    <footer v-if="!isLoginPage" class="bg-white border-t border-light-border mt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <p class="text-center text-medium-gray text-sm">
          &copy; {{ new Date().getFullYear() }} Kenya Red Cross Society. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'

const mobileMenuOpen = ref(false)
const dashboardDropdownOpen = ref(false)
const dashboardDropdownRef = ref(null)
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isLoginPage = computed(() => route.name === 'Login')
const isDashboardActive = computed(() => route.path === '/dashboard' || route.path === '/matrix')

const switchDashboard = (target) => {
  dashboardDropdownOpen.value = false
  router.push(target)
}

const handleLogout = async () => {
  mobileMenuOpen.value = false
  await authStore.logout()
}

const handleOutsideClick = (e) => {
  if (dashboardDropdownRef.value && !dashboardDropdownRef.value.contains(e.target)) {
    dashboardDropdownOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleOutsideClick))
onUnmounted(() => document.removeEventListener('click', handleOutsideClick))
</script>

<style scoped>
.nav-link {
  @apply text-charcoal font-medium hover:text-red-primary transition-colors duration-200 pb-1 border-b-2 border-transparent;
}

.nav-link-active {
  @apply text-red-primary border-red-primary;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
