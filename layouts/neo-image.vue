<script setup lang="ts">
import { computed } from 'vue'
import { resolveAssetUrl } from '@slidev/client/layoutHelper.ts'

const props = defineProps({
  image: { type: String, default: '' },
  title: { type: String, default: 'image.png' },
})

const bgStyle = computed(() => ({
  backgroundImage: props.image ? `url("${resolveAssetUrl(props.image)}")` : 'none',
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
}))
</script>

<template>
  <div class="slidev-layout neo-image h-full flex flex-col bg-[#C0C0C0] relative overflow-hidden">
    <MacMenuBar />
    <div class="flex-1 flex flex-col mx-2 mb-1 mt-0">
      <div class="mac-window flex-1 flex flex-col">
        <div class="mac-titlebar">
          <div class="mac-close-box" />
          <span class="mac-titlebar-title">{{ title }}</span>
        </div>
        <div class="flex-1 relative overflow-hidden" :style="bgStyle">
          <div class="absolute bottom-0 left-0 right-0 bg-black/70 px-6 py-4 text-white">
            <slot />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
