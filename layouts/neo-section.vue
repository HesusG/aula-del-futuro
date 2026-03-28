<template>
  <div class="slidev-layout neo-section h-full flex flex-col items-center justify-center bg-[#A0A0A0] relative">
    <!-- CRT Monitor Frame -->
    <div class="crt-bezel w-[95%] max-w-6xl" style="overflow: visible;">
      <div class="crt-screen px-8 py-10 text-center relative" style="overflow: visible;">
        <div class="crt-scanlines overflow-hidden" />
        <div class="relative z-10">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>
