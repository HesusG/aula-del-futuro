<template>
  <div class="slidev-layout neo-cover h-full flex flex-col bg-[#C0C0C0] relative overflow-hidden">
    <MacMenuBar />
    <!-- Centered Mac Window -->
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="mac-window max-w-3xl w-full">
        <div class="mac-titlebar">
          <div class="mac-close-box" />
          <span class="mac-titlebar-title">Mas alla de SQL</span>
        </div>
        <div class="mac-window-content text-center px-12 py-10">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>
