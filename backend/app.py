
from flask import Flask, request, jsonify

from pymongo import MongoClient
import data_processing
import impl
import os
import infer
import sonar
import json

app = Flask(__name__)

@app.route('/')
def getData():
    col = connectDB()
    result = data_processing.filter({},col)
    return result

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/project',methods=['post'])
def add_stu():
    if  not request.query_string:  
        return ('fail')
    address = request.query_string
    return(address)


# eclipse%2Fditto
# gitProject>/<userToken>
# {
# 	"gitProject": "eclipse/ditto",
# 	"userToken": ""
# }
@app.route('/getRelease', methods = ['POST'])
def getRelease():
     if request.method == 'POST':
        data = request.json # a multidict containing POST data
        print(data)
        releases = impl.getGitReleases(data["gitProject"], data["userToken"])
        list = []
        for value in releases:
            list.append(str(value)[10:])

        return json.dumps(list)

@app.route('/process/<chosenRelease>/<changeDirectory>')
def process(chosenRelease, changeDirectory):
    changeDirectory = '../'+ changeDirectory
    os.chdir(changeDirectory)
    os.system("git checkout tags/"+chosenRelease) 

    # 2. Analyze the project with infer and sonar -----------------------------------
    sonar.sonar_analyze()
    infer.infer_analyze()

@app.route('/test/<message>')
def testMessage(message):
    return message

def connectDB():
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
    client = MongoClient(CONNECTION_STRING)
    db= client.issues
    col = db.issues
    return col