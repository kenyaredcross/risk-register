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
              <router-link
                to="/"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/' }"
              >
                Dashboard
              </router-link>
              <router-link
                to="/risks"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/risks' }"
              >
                Risk Register
              </router-link>
              <router-link
                v-if="authStore.isSystemManager"
                to="/admin/departments"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path.startsWith('/admin') }"
              >
                Admin
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
          <router-link to="/" class="block py-2 text-charcoal hover:text-red-primary" @click="mobileMenuOpen = false">
            Dashboard
          </router-link>
          <router-link to="/risks" class="block py-2 text-charcoal hover:text-red-primary" @click="mobileMenuOpen = false">
            Risk Register
          </router-link>
          <router-link v-if="authStore.isSystemManager" to="/admin/departments" class="block py-2 text-charcoal hover:text-red-primary" @click="mobileMenuOpen = false">
            Admin
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
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from './stores/authStore'

const mobileMenuOpen = ref(false)
const route = useRoute()
const authStore = useAuthStore()

const isLoginPage = computed(() => route.name === 'Login')

const handleLogout = async () => {
  mobileMenuOpen.value = false
  await authStore.logout()
}
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
