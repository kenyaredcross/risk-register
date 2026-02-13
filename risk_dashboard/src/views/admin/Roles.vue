<template>
  <div class="animate-fade-in">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-charcoal mb-2">Administration</h1>
      <p class="text-medium-gray">Manage departments, users, and roles</p>
    </div>

    <!-- Admin Navigation Tabs -->
    <div class="mb-6 border-b border-light-border">
      <nav class="flex space-x-6">
        <router-link
          to="/admin/departments"
          class="pb-3 px-1 border-b-2 font-medium text-sm transition-colors"
          :class="$route.path === '/admin/departments' ? 'border-red-primary text-red-primary' : 'border-transparent text-medium-gray hover:text-charcoal hover:border-light-border'"
        >
          Departments & Units
        </router-link>
        <router-link
          to="/admin/users"
          class="pb-3 px-1 border-b-2 font-medium text-sm transition-colors"
          :class="$route.path === '/admin/users' ? 'border-red-primary text-red-primary' : 'border-transparent text-medium-gray hover:text-charcoal hover:border-light-border'"
        >
          Users
        </router-link>
        <router-link
          to="/admin/roles"
          class="pb-3 px-1 border-b-2 font-medium text-sm transition-colors"
          :class="$route.path === '/admin/roles' ? 'border-red-primary text-red-primary' : 'border-transparent text-medium-gray hover:text-charcoal hover:border-light-border'"
        >
          Roles Reference
        </router-link>
      </nav>
    </div>

    <div class="mb-6">
      <h2 class="text-xl font-bold text-charcoal mb-1">KRCS Roles Reference</h2>
      <p class="text-sm text-medium-gray">Reference guide for KRCS Risk Management roles and their permissions</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Global Approvers -->
      <div class="card">
        <div class="flex items-center space-x-2 mb-4">
          <div class="w-3 h-3 rounded-full bg-green-500"></div>
          <h3 class="text-lg font-bold text-charcoal">Global Approvers</h3>
        </div>
        <p class="text-sm text-medium-gray mb-4">Can approve/reject any risk regardless of department or project</p>
        <div class="space-y-2">
          <div class="bg-light-gray rounded p-3">
            <div class="font-semibold text-charcoal">KRCS HOR</div>
            <div class="text-xs text-medium-gray mt-1">Head of Region - Global approval authority</div>
          </div>
          <div class="bg-light-gray rounded p-3">
            <div class="font-semibold text-charcoal">KRCS DSG</div>
            <div class="text-xs text-medium-gray mt-1">Director of Strategic Goals - Global approval authority</div>
          </div>
        </div>
      </div>

      <!-- Department-Scoped Approvers -->
      <div class="card">
        <div class="flex items-center space-x-2 mb-4">
          <div class="w-3 h-3 rounded-full bg-blue-500"></div>
          <h3 class="text-lg font-bold text-charcoal">Department-Scoped Approvers</h3>
        </div>
        <p class="text-sm text-medium-gray mb-4">Can only approve risks in their own department</p>
        <div class="space-y-2">
          <div class="bg-light-gray rounded p-3">
            <div class="font-semibold text-charcoal">KRCS HOD</div>
            <div class="text-xs text-medium-gray mt-1">Head of Department - Approves risks in their department only</div>
          </div>
        </div>
      </div>

      <!-- Project-Scoped Approvers -->
      <div class="card">
        <div class="flex items-center space-x-2 mb-4">
          <div class="w-3 h-3 rounded-full bg-purple-500"></div>
          <h3 class="text-lg font-bold text-charcoal">Project-Scoped Approvers</h3>
        </div>
        <p class="text-sm text-medium-gray mb-4">Can only approve risks on their own projects</p>
        <div class="space-y-2">
          <div class="bg-light-gray rounded p-3">
            <div class="font-semibold text-charcoal">KRCS Project Manager</div>
            <div class="text-xs text-medium-gray mt-1">Approves risks on projects they manage</div>
          </div>
        </div>
      </div>

      <!-- Risk Contributors -->
      <div class="card">
        <div class="flex items-center space-x-2 mb-4">
          <div class="w-3 h-3 rounded-full bg-orange-500"></div>
          <h3 class="text-lg font-bold text-charcoal">Risk Contributors</h3>
        </div>
        <p class="text-sm text-medium-gray mb-4">Can create and edit risks, submit for approval</p>
        <div class="space-y-2">
          <div class="bg-light-gray rounded p-2">
            <div class="text-sm font-medium text-charcoal">KRCS RPC</div>
            <div class="text-xs text-medium-gray">Risk Program Coordinator</div>
          </div>
          <div class="bg-light-gray rounded p-2">
            <div class="text-sm font-medium text-charcoal">KRCS Finance Officer</div>
            <div class="text-xs text-medium-gray">Finance Department</div>
          </div>
          <div class="bg-light-gray rounded p-2">
            <div class="text-sm font-medium text-charcoal">KRCS Procurement Manager</div>
            <div class="text-xs text-medium-gray">Procurement Department</div>
          </div>
          <div class="bg-light-gray rounded p-2">
            <div class="text-sm font-medium text-charcoal">KRCS Logistics Manager</div>
            <div class="text-xs text-medium-gray">Logistics Department</div>
          </div>
          <div class="bg-light-gray rounded p-2">
            <div class="text-sm font-medium text-charcoal">KRCS HR Manager</div>
            <div class="text-xs text-medium-gray">Human Resources Department</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Workflow Info -->
    <div class="card mt-6">
      <h3 class="text-lg font-bold text-charcoal mb-4">Approval Workflow</h3>
      <div class="space-y-4">
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm font-bold text-charcoal">1</div>
          <div>
            <div class="font-semibold text-charcoal">Draft / Rejected</div>
            <div class="text-sm text-medium-gray">Any user can create and edit risks in this state</div>
          </div>
        </div>
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0 w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center text-sm font-bold text-orange-700">2</div>
          <div>
            <div class="font-semibold text-charcoal">Pending Approval</div>
            <div class="text-sm text-medium-gray">Submitted for approval - locked for editing. Eligible approvers can approve or reject.</div>
          </div>
        </div>
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-sm font-bold text-green-700">3</div>
          <div>
            <div class="font-semibold text-charcoal">Open</div>
            <div class="text-sm text-medium-gray">Approved and active. Users can request closure when risk is mitigated.</div>
          </div>
        </div>
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0 w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center text-sm font-bold text-orange-700">4</div>
          <div>
            <div class="font-semibold text-charcoal">Pending Close Approval</div>
            <div class="text-sm text-medium-gray">Closure requested - locked for editing. Eligible approvers can approve (close) or reject (reopen).</div>
          </div>
        </div>
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-sm font-bold text-blue-700">5</div>
          <div>
            <div class="font-semibold text-charcoal">Closed</div>
            <div class="text-sm text-medium-gray">Risk is closed and archived. Locked for editing.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Read-only reference page - no API calls needed
</script>
