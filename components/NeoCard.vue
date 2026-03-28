<script setup>
defineProps({
  color: { type: String, default: 'white' },
  title: { type: String, default: '' },
  noChrome: { type: Boolean, default: false },
})
</script>

<template>
  <div v-if="noChrome" class="border-2 border-black p-5 shadow-[2px_2px_0px_#000]" :class="`bg-${color}`">
    <slot />
  </div>
  <div v-else class="mac-window">
    <div class="mac-titlebar">
      <div class="mac-close-box" />
      <span v-if="title" class="mac-titlebar-title">{{ title }}</span>
    </div>
    <div class="mac-window-content" :class="`bg-${color}`">
      <slot />
    </div>
  </div>
</template>
