<template>
  <div class="slidev-layout h-full flex flex-col bg-[#C0C0C0] relative overflow-hidden">
    <MacMenuBar />
    <div class="flex-1 flex flex-col mx-1 mb-1 mt-0 bg-white border-2 border-black px-4 py-2 overflow-hidden">
      <slot />
    </div>
  </div>
</template>
