<template>
  <div id="app" class="min-h-screen bg-off-white">
    <!-- Header -->
    <header class="bg-white shadow-elegant sticky top-0 z-50">
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
            </nav>

            <!-- Add Risk Button -->
            <a
              href="/app/program-risk-register/new-program-risk-register-1"
              target="_blank"
              class="flex items-center space-x-1 bg-red-primary hover:bg-red-dark text-white px-4 py-2 rounded-lg transition-colors duration-200 font-medium shadow-sm hover:shadow-md"
              title="Add New Risk"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              <span>Add Risk</span>
            </a>
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
          <router-link to="/" class="block py-2 text-charcoal hover:text-red-primary" @click="mobileMenuOpen = false">
            Dashboard
          </router-link>
          <router-link to="/risks" class="block py-2 text-charcoal hover:text-red-primary" @click="mobileMenuOpen = false">
            Risk Register
          </router-link>
          <a
            href="/app/program-risk-register/new-program-risk-register-1"
            target="_blank"
            class="flex items-center space-x-2 bg-red-primary hover:bg-red-dark text-white px-4 py-2 rounded-lg transition-colors duration-200 font-medium mt-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>Add Risk</span>
          </a>
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

    <!-- Footer -->
    <footer class="bg-white border-t border-light-border mt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <p class="text-center text-medium-gray text-sm">
          &copy; {{ new Date().getFullYear() }} Kenya Red Cross Society. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const mobileMenuOpen = ref(false)
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
