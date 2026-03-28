<template>
  <div class="slidev-layout neo-demo h-full flex flex-col bg-[#C0C0C0] relative overflow-hidden">
    <MacMenuBar />
    <!-- Mac Window wrapping terminal -->
    <div class="flex-1 flex flex-col mx-1 mb-1 mt-0">
      <div class="mac-window flex-1 flex flex-col">
        <div class="mac-titlebar">
          <div class="mac-close-box" />
          <span class="mac-titlebar-title">Terminal</span>
          <span class="absolute right-2 text-[#2DD4BF] text-xs font-mono font-bold px-2 py-0 border border-[#2DD4BF] bg-[#282A36] rounded-sm" style="font-size:0.6rem;">LIVE</span>
        </div>
        <div class="flex-1 flex flex-col bg-[#282A36] text-[#F8F8F2] overflow-hidden">
          <div class="flex-none px-4 py-2">
            <slot name="title" />
          </div>
          <div class="flex-1 overflow-auto px-4 pb-3">
            <slot />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
