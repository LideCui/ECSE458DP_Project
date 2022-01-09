<template>
  <div id="main">
    <h2>Data Base</h2>
    <ul>
      <a href="http://localhost:8080/#/" target="_blank">SoftVali</a>
      
    </ul>

    
    <table id="vuln-table">
      <tr>
        <th>ID</th>
        <th>Bug type</th>
        <th>Description</th>
        <th>False alarm</th>
        <th>File</th> 
        <th>Line</th>
        <th>Release version</th>
        <th>Severity</th>
        <th>Source</th>
      </tr>

    <tr v-for="(vuln, i) in vulns" v-bind:key="`vuln-${i}`" >
      <td>{{ vuln._id }}</td>
      <td>{{ vuln.bug_type }}</td>
      <td>{{ vuln.description }}</td>
      <td>{{ vuln.false_alarm }}</td>
      <td>{{ vuln.file }}</td>
      <td>{{ vuln.line }}</td>
      <td>{{ vuln.release_version }}</td>
      <td>{{ vuln.serverity }}</td>
      <td>{{ vuln.source }}</td>
    </tr>
  

    </table>


   <!-- <p>
     This is vulnerabilities
     {{vulns}}
   </p>  -->
   

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

