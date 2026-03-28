<template>
  <div class="mac-menu-bar">
    <span>&#9632; File</span>
    <span>Edit</span>
    <span>View</span>
    <span>Special</span>
    <!-- Battery indicator -->
    <span class="ml-auto flex items-center gap-1 text-xs font-mono">
      <span>{{ Math.round(($slidev.nav.currentPage / $slidev.nav.total) * 100) }}%</span>
      <span class="battery-shell">
        <span
          class="battery-fill"
          :style="{
            width: Math.round(($slidev.nav.currentPage / $slidev.nav.total) * 100) + '%',
            background: Math.round(($slidev.nav.currentPage / $slidev.nav.total) * 100) >= 75
              ? '#2DD4BF'
              : Math.round(($slidev.nav.currentPage / $slidev.nav.total) * 100) <= 20
                ? '#FF6B6B'
                : '#808080',
          }"
        />
      </span>
    </span>
  </div>
</template>

<style scoped>
.battery-shell {
  display: inline-block;
  width: 20px;
  height: 10px;
  border: 2px solid #000;
  position: relative;
  background: #fff;
}
.battery-shell::after {
  content: '';
  position: absolute;
  right: -5px;
  top: 1px;
  width: 3px;
  height: 4px;
  background: #000;
  border-radius: 0 1px 1px 0;
}
.battery-fill {
  display: block;
  height: 100%;
  transition: width 0.3s ease;
}
</style>
