<template>
  <div class="slidev-layout neo-two-cols h-full flex flex-col bg-[#C0C0C0] relative overflow-hidden">
    <MacMenuBar />
    <div class="flex-1 flex flex-col m-4 mt-2">
      <div class="mac-window flex-1 flex flex-col">
        <div class="mac-titlebar">
          <div class="mac-close-box" />
        </div>
        <div class="mac-window-content flex-1 flex flex-col">
          <div class="mb-4">
            <slot name="title" />
          </div>
          <div class="flex-1 grid grid-cols-2 gap-0">
            <div class="border-r-2 border-black pr-4">
              <slot name="left" />
            </div>
            <div class="pl-4">
              <slot name="right" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
