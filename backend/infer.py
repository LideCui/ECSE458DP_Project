# run infer by infer.py
import sys
import subprocess
from github import Github
from pymongo import MongoClient
import json
import uuid
import os

def printf(format, *args):
    sys.stdout.write(format % args)

# return path directory
def parseInputToPath(args):
    return args[1]

def getGitReleases(args):
    # Put your GitHub token here

    G = Github("")  
    repo = G.get_repo("eclipse/paho.mqtt.java")
    releases = repo.get_releases()
    for release in releases:
        print(release)

def write2DB(file):
    # Step 1. connect to MongoDB, and add a new database called "vurlnerability"
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
    client = MongoClient(CONNECTION_STRING)
    db= client.issues
    col = db.issues # infer, sonar

    # Step 2. clean given data
    data = []

    ## handle infer
    with open(file) as read_file:
        res_infer = json.loads(read_file.read())

    for issue in res_infer:
        data_template = {
            '_id': 0,
            'bug_type': "",
            'description': "",
            'serverity': "",
            'line': -1,
            'file': "",
        # customized parameters
            'release_version': "XX.XX.XX",
            'false_alarm': False,
            'source': "Infer",
        }
        data_template['_id'] = str(uuid.uuid4())
        data_template['bug_type'] = issue['bug_type']
        data_template['description'] = issue["qualifier"]
        data_template['serverity'] = issue["severity"]
        data_template['line'] = issue["line"]
        data_template['file'] = issue["file"]
        data.append(data_template)

    # Step 3. insert data into db
    result = col.insert_many(data)
    cursor = col.find()
    for item in cursor:
        print(item)

def infer_analyze():
    # changeDirectory = "cd ./paho.mqtt.java"
    # path = parseInputToPath(sys.argv)
    path = input("Input your infer target path: ")
    path = '../'+path
    os.chdir(path)

    runInfer="infer run -o ../output -- mvn compile -DskipTests -Dlicense.skip=true"
    os.system(runInfer)

    # getGitReleases(sys.argv)

if __name__ == '__main__':
    infer_analyze()