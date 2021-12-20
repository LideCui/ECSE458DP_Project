# run infer by infer.py
import sys
import subprocess
import requests
from requests.auth import HTTPBasicAuth

# def printf(format, *args):
#     sys.stdout.write(format % args)

if __name__ == '__main__':
    # changeDirectory = "cd ./paho.mqtt.java"
    # runInfer="infer analyze -- mvn verify -DskipTests"
    # subprocess.call(runInfer.split(), cwd="./paho.mqtt.java")
    
    r = requests.get('http://localhost:9000/api/issues/search?componentKeys=Eclipse-Ditto&types=VULNERABILITY',
                        auth=HTTPBasicAuth('admin', 'changzichen251'))
    print("before")
    print(r.text)
    print("helloworld")
    # sys.exit()