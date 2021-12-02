# run infer by infer.py
import sys
import subprocess

def printf(format, *args):
    sys.stdout.write(format % args)

if __name__ == '__main__':
    changeDirectory = "cd ./paho.mqtt.java"
    runInfer="infer analyze -- mvn verify -DskipTests"
    subprocess.call(runInfer.split(), cwd="./paho.mqtt.java")
    sys.exit()