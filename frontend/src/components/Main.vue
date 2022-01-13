<template>
  <div id="main">
    <h2>Data Base</h2>
    <ul>
      <a href="http://localhost:8080/#/" target="_blank">SoftVali</a>
      
    </ul>

    <div id = "table">
    <table id="vuln-table">
      <tr>
        
        <th>ID</th>
        <th>Bug type</th>
        <th>Description</th>
        <th>False alarm</th>
        <!-- <th>File</th>  -->
        <th>Line</th>
        <th>Release version</th>
        <th>Severity</th>
        <th>Source</th>
        <!-- <th>File</th>  -->

      </tr>

    <tr v-for="(vuln, i) in vulns" v-bind:key="`vuln-${i}`" >
      <td>{{ vuln._id }}</td>
      <td>{{ vuln.bug_type }}</td>
      <td>{{ vuln.description }}</td>
      <td>{{ vuln.false_alarm }}</td>
      <!-- <td>{{ vuln.file }}</td> -->
      <td>{{ vuln.line }}</td>
      <td>{{ vuln.release_version }}</td>
      <td>{{ vuln.serverity }}</td>
      <td>{{ vuln.source }}</td>
      <!-- <td>{{ vuln.file }}</td> -->
    </tr>
  

    </table>
    </div>


   <p>
     Testing connection
     {{message}}
   </p> 
   

  </div>
</template>

<script src="./database.js">

</script>



<style>
  #main {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    color: #2c3e50;
    background: #ffffff;
  }
 

  th,
  td { padding: 10px 10px; }

  #table {
    text-align: center;
    /* width: 100%; */
  }

  table { border-collapse: collapse; }
  tr { border-bottom: solid 1px #0a0707; }

  th,
  td { text-align: center; }
</style>

