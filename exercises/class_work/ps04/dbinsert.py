import json

def insert_data(data, db):

    # Your code here. Insert the data into a collection 'arachnid'

    for value in data:
        db.arachnid.insert(value)


if __name__ == "__main__":

    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    with open('/Users/Darshan/Documents/Data-Wrangle-OpenStreetMaps-Data/data/arachnid.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
        print db.arachnid.find_one()