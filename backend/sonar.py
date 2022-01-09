# run infer by infer.py
import sys
import requests
import json
from requests.auth import HTTPBasicAuth
import os

# local credentials
login = ''
pin = ''
projectKey = ''
types = ''

def sonar_analyze():
    login = input("Your Sonar Login: ")
    pin = input("Your Sonar pin: ")
    projectKey = input("Your target project: ")
    types = input("Your target types: ")

    # create a http request to retrieve the vulnerabilities of a project
    try:
        url = 'http://localhost:9000/api/issues/search?componentKeys='+projectKey+'&types='+types
        r = requests.get(url, auth=HTTPBasicAuth(login, pin))
        
        data = json.loads(r.text)   # response text body is already a json, just load it
        print(data)
        
        # Document:
        #
        # r = requests.get('http://localhost:9000/api/issues/search?componentKeys=Eclipse-Ditto&types=VULNERABILITY',
        #                 auth=HTTPBasicAuth('admin', 'changzichen251'))
        
    except:
        sys.exit("Connection could not be established") 

    print('Writing to the data.json...')
    # output the json file of the response

    filename = "./output/sonar_report.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
        
    # with open('data.json', 'w') as f:
    #     json.dump(data, f, indent=4)
    print('...Done')



if __name__ == '__main__':  
    sonar_analyze()