import axios from 'axios'
//import * as AxiosLogger from 'axios-logger';




var config = require('../../config')

var frontendUrl = 'http://' + config.dev.host + ':' + config.dev.port
//var backendUrl = 'http://' + config.dev.backendHost + ':' + config.dev.backendPort

var backendUrl = 'http://127.0.0.1:5000';

var AXIOS = axios.create({
  baseURL: backendUrl,
  headers: { 'Access-Control-Allow-Origin': frontendUrl }
})

export default{
    name:'database',
    
    data () {
        return {
            vulns:[],
            errorVuln:'',
            message:'',
            joker:'i am joker'
        }
    },

    created: function(){
        AXIOS.get('/')
        .then(response => {this.vulns = response.data})
        .catch(e => {this.errorVuln = e});

        AXIOS.get('/hello')
        .then(response => {this.message = response.data})
        .catch(e => {this.errorVuln = e});
    }

}
