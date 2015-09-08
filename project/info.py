def getDatabase():
    return "example"


def getCollection():
    return "test"

def getMongoClient(url):
    from pymongo import MongoClient
    client = MongoClient(url)
    return client