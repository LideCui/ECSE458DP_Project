<template>
  <div id="sa">
    <h2>Static Analyser</h2>
    <ul>
      <a href="http://localhost:8080/#/" target="_blank">SoftVali</a>
    </ul>

    <div id = "SA-input">
    <input id="address" type="text" v-model="address" placeholder="Github Project Address">
    </div>

    <div id = "SA-input">
    <input id="usertoken" type="text" v-model="token" placeholder="User Token">
    </div>

    <button id="send" v-bind:disabled="!address" v-on:click="sendAddress(address)">Send</button>

    <p>
        Address: {{address}}
        <br>
        Token: {{token}}

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

  #SA-input {
    width: 80%;
  }
</style>