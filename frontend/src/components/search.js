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
            token:'',
            releases:[],
            output:'',
            chosenRelease:'',
            errorAddress:'',
            requestBody: {
                gitProject: '',
 	            userToken: ''
            },
            errorReleases: '',
            testConnection:''
        }
    },

    created: function(){
        AXIOS.get('/hello')
        .then(response => {this.testConnection = response.data})
        .catch(e => {this.errorVuln = e});
    },

    methods:{
        getReleases: function(address, token){
            this.requestBody.gitProject = address;
            this.requestBody.userToken = token;

            AXIOS.post('/getRelease', this.requestBody)
                .then(response => {
                this.releases = response.data;
                this.output = response.data;

            })
            .catch(e => {
                e = e.response.data.message ? e.response.data.message : e;
                this.errorReleases = e;
                console.log(e);
            });

        },

        sendRelease: function(chosenRelease){
           
            //AXIOS.post().then({}).catch({})
        }
    }
}
