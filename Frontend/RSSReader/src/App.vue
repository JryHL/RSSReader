<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <div class="toolbar">
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/add">Add a source</RouterLink>
        </div>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
.toolbar {
  display: flex;
  flex-direction: row;
  background-color: rgba(0,0,0,0.1);
  gap: 5px;
  font-size: 1.3em;
  font-family: sans-serif;
}
</style>
