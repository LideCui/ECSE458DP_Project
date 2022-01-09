<template>
  <div id="sa">
    <h2>Static Analyser</h2>
    <ul>
      <a href="http://localhost:8080/#/" target="_blank">SoftVali</a>
    </ul>

    <input id="address" type="text" v-model="address" placeholder="Project Address">
    <button id="send" v-bind:disabled="!address" v-on:click="sendAddress(address)">Send</button>

    <p>
        Input: {{address}}
    </p>

  </div>

</template>

<script src="./static.js">

</script>


<style>
  #sa {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    color: #2c3e50;
    background: #f2ece8;
  }
</style>