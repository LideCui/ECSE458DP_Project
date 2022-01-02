from pymongo import MongoClient

if __name__ == '__main__':
    # Step 1. connect to MongoDB, and add a new database called "vurlnerability"
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
    client = MongoClient(CONNECTION_STRING)
    db= client.issues
    col = db.issues # infer, sonar

    # debug purpose code
    print(client.list_database_names())
    print(db.list_collection_names())
    '''
    serverStatusResult=db.command("serverStatus")
    pprint(serverStatusResult)
    '''

