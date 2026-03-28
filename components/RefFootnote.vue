<script setup>
defineProps({
  sources: { type: Array, required: true },
})
</script>

<template>
  <div class="ref-footnote">
    <span v-for="(src, i) in sources" :key="i">
      <span v-if="i > 0"> | </span>
      {{ src }}
    </span>
  </div>
</template>
