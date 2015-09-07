import pprint

def get_client():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    return client

def get_db():
    client = get_client()
    db = client.examples
    return db


def insert_course(db,course_info):
    result = db.edx.insert_one(course_info)
    result.inserted_id

def find_course(db,course_name):
    projection = {"_id" : 0,"course_uni" : 1,'course_len':1}
    result = db.edx.find({'course_name' : course_name},projection)
    print_result(result)

def print_result(result):
 for course in result:
    pprint.pprint(course)

def find_total_count(db):
    print db.edx.find().count()

def find_course_with_length(db):
    query = {"course_len" : { "$gte" : 15}}
    result = db.edx.find(query)
    print_result(result)

def find(db):
    query = {"course_year" : 2015}
    result = db.edx.find_one(query)
    result['course_year'] = 2016
    db.edx.save(result)
    print_result(result)


if __name__ == "__main__":
    client = get_client()
    db = client.twitter
    print db.tweets.find().count()




