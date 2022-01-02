from flask import jsonify

# filter by user preference
def filter(args, col):
    cursor = col.find(args)
    result = []
    for item in cursor:
        result.append(item)
        print(item)
    return jsonify(result)

def count(col):
    count = col.find().count()
    print(count)
    return count