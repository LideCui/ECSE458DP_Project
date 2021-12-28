
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import json

# Step 1. connect to MongoDB, and add a new database called "vurlnerability"
CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
client = MongoClient(CONNECTION_STRING)
db= client.vulnerability
# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)

# Step 2. clean given data
## handle infer
with open("./report.json") as read_file:
    res_infer = json.loads(read_file)
    
print(res_infer["bug_type"])

## handle sonarqube

# Step 3. insert data into db


