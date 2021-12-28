
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import json
import uuid

# Step 1. connect to MongoDB, and add a new database called "vurlnerability"
CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
client = MongoClient(CONNECTION_STRING)
db= client.issues
col = db.issues


# debug purpose code
'''
print(client.list_database_names())
print(db.list_collection_names())
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)
'''

# Step 2. clean given data
data = []

## handle infer
with open("./report.json") as read_file:
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

## handle sonarqube
with open("./SonarQubeResponseBUG.json") as read_file:
    res_sonar = json.loads(read_file.read())["issues"]

for issue in res_sonar: 
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
    data_template['bug_type'] = issue['rule']
    data_template['description'] = issue["message"]
    data_template['serverity'] = issue["severity"]
    data_template['line'] = issue["line"]
    data_template['file'] = issue["component"]
    data.append(data_template)

# Step 3. insert data into db
result = col.insert_many(data)
cursor = col.find()

for item in cursor:
    print(item)