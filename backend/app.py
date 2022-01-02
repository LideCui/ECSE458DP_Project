from flask import Flask
from pymongo import MongoClient
import data_processing

app = Flask(__name__)

@app.route("/")
def hello_world():
    col = connectDB()
    result = data_processing.filter({},col)
    return result

def connectDB():
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
    client = MongoClient(CONNECTION_STRING)
    db= client.issues
    col = db.issues
    return col