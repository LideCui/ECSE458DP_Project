<template>
    <div id="main_search">
        <h2>Search</h2>
        <ul>
        <a href="http://localhost:8080/#/" target="_blank">SoftVali</a>
        </ul>
        <div id = "search_bar">
        <input id="address" type="text" v-model="address" placeholder="Project Address">
        <br>
        <input id="token" type="text" v-model="token" placeholder="User token">
        <br>
        <p>
            Address: {{address}}
            <br>
            Token: {{token}}
        </p>

        <button id="send_address" v-bind:disabled="!address" v-on:click="getReleases(address,token)">Get releases</button>
        </div>
        
        <p>
           Available release version:  {{releases}}
           <br>
           Error message: {{errorReleases}}
           <br>
           Connection: {{testConnection}}
        </p>

        <div id = "search_bar2">
       
        <select id='release' v-model="chosenRelease">
            <option disabled value="">Please select release</option>
            <option v-for="(release, i) in releases" v-bind:key="`release-${i}`">{{releases[i]}}</option>
        </select>
        <br>
        <p>
            Chosen release: {{chosenRelease}}
        </p>
        <button id="send_release" v-bind:disabled="!chosenRelease" v-on:click="sendRelease(release)">Send</button>
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

   #token {
       width: 50%
   }

   #release {
       width: 50%
   }
</style>
