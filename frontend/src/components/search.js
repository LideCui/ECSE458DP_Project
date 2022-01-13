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
    name:'search',
    
    data () {
        return {
            address:'',
            errorAddress:'',
            release:''

        }
    },
    methods:{
  
    }
}
