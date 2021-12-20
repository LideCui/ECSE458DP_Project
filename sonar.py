# run infer by infer.py
import sys
import os


if __name__ == '__main__':
    runSonar = "curl -u admin:0333 \"http://localhost:9000/api/issues/search?" \
               "componentKeys=paho.mqtt.java&types=VULNERABILITY\""
    os.system(runSonar)
    sys.exit()
    print("hello")
