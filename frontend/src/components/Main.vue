<template>
  <div id="main">
    <h2>Data Base</h2>
    <ul>
      <a href="http://localhost:8080/#/" target="_blank">SoftVali</a>
      
    </ul>


   <p>
     This is vulnerabilities
     {{vulns}}
   </p> 
   <p>
     This is test connection
     {{message}}
   </p> 
   <p>
     variable:
     {{joker}}
     {{backendUrl}}
   </p> 

<!-- <table>
  <tr v-for="vuln in vulns" >
      <td>{{ person.name }}</td>
      
  </tr>
     </table>
-->

  </div>
</template>

<script src="./database.js">

</script>



<style>
  #main {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    color: #2c3e50;
    background: #f2ece8;
  }
</style>

