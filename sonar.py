# run infer by infer.py
import sys
import subprocess
import requests
import json
from requests.auth import HTTPBasicAuth

# def printf(format, *args):
#     sys.stdout.write(format % args)

projectKey = ''
types = ''

if __name__ == '__main__':  

    # create a http request to retrieve the vulnerabilities of a project
    r = requests.get('http://localhost:9000/api/issues/search?componentKeys=Eclipse-Ditto&types=VULNERABILITY',
                        auth=HTTPBasicAuth('admin', 'changzichen251'))


    print('================================================================')
    data = json.loads(r.text)   # response text body is already a json, just load it
    print(data)
    print('================================================================')

    # output the json file of the response
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    # sys.exit()