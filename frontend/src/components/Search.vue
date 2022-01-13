<template>
    <div id="main_search">
        <h2>Search</h2>
        <ul>
        <a href="http://localhost:8080/#/" target="_blank">SoftVali</a>
        </ul>
        <div id = "search_bar">
        <input id="address" type="text" v-model="address" placeholder="Project URL">
        <button id="send_address" v-bind:disabled="!address" v-on:click="sendAddress(address)">Send</button>
        </div>
        
        <p>
           Available release version:  
        </p>

        <div id = "search_bar2">
        <input id="release" type="text" v-model="release" placeholder="Release Version">
        <button id="send_release" v-bind:disabled="!release" v-on:click="sendRelease(address)">Send</button>
        </div>
    </div>
</template>

<script src="./search.js">

</script>

<style scoped>
  #main_search {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    color: #2c3e50;
    background: #ffffff;

  }

   #address {
       width: 50%
   }

   #release {
       width: 50%
   }
</style>
