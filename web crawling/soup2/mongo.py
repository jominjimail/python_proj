import pymongo
import datetime
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId
import json


client = MongoClient('localhost',27017)

db = client.test_database
collection = db.test_collection


post ={
    "author":"Mike",
    "text":"My first blog post!",
    "tags":["mongodb","python","pymongo"],
    "date": datetime.datetime.utcnow()
}

posts = db.posts
post_id = posts.insert(post)
pprint.pprint(posts.find_one({"author":"Mike"}))

def get(post_id):
    documnet = client.db.collection.find_one({'_id':ObjectId(post_id)})