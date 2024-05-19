<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <div class="toolbar">
          <RouterLink class="roboto page-nav-btn" :to="{name:'recommended'}">Home</RouterLink>

          <RouterLink class="roboto page-nav-btn" :to="{name:'sourcelist'}">RSS Feeds</RouterLink>
          
        </div>
      </nav>
    </div>
  </header>
  <div class="contentsView">
    <RouterView/>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  flex-direction: row;
  background-color: rgb(240, 240, 240);
  width: 100%;
  font-size: 1.3em;
  font-family: sans-serif;
  position:fixed;
  top: 0px;
  box-shadow: 0px 2px 4px rgba(0,0,0,0.3);
}
.page-nav-btn {
  color: black;
  text-decoration: none;
  height: 100%;
  padding: 5px;
  transition: 0.2s;
  border-right: 1px solid rgba(0,0,0,0.3);
}
.page-nav-btn:hover {
  background-color: rgb(220, 220, 220);
}

.contentsView {
  margin-top: 25px;
}
</style>
