from pymongo import MongoClient

mongo_client = MongoClient(
        host="my_mongo",
        port=27017,
        username="admin",
        password="pass"
        )
