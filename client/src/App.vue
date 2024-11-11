<template>
  <div id="app">
    <DashBoard />
  </div>
</template>

<script>
import DashBoard from './components/DashBoard.vue';

export default {
  name: 'App',
  components: {
    DashBoard,
  },
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f9;
  margin: 0;
  padding: 20px;
}     
</style>
