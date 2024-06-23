from pymongo import MongoClient
from pprint import pprint
import pandas as pd
import json

# CONNECT to MongoDB
client = MongoClient(
    host="my_mongo",
    port = 27017,
    username="admin", 
    password="pass"
)

# READ data extracted previously from the website Capterra and transformed
df = pd.read_csv("../../data_csv/capterra.csv")

# CREATE new database with new collection
mydb = client["webSites"]
mycol = mydb["Capterra"]

# LOAD data into MongoDB
mycol.delete_many({})  # Destroy the collection
out = mycol.insert_many(df.to_dict('records'))
print("Available databases: ", client.list_database_names())
print("Created collection: ", mydb.list_collection_names())

# print single document from this collection
print()
print("==========Single Document Exemple==========")
print("Single document example:")
pprint(list(mycol.find())[30000])
print("===========================================")
print()

print("The Capterra collections contains:")
print()
# TOTAL number of documents
#print("{} documents".format(len(list(mycol.find()))))
print("{} documents".format(mycol.count_documents({})))
print()
# GET only the documents with 'date_experience' >12 months
l = list(mycol.aggregate([ {"$match":{"date_experience":{"$gt":12}}}  ]))
print("{} documents with 'date_experience' > 12 months".format(len(l)))
print()
# GET only the documents with 'date_experience' >12 months
l = list(mycol.aggregate([ {"$match":{"$and":[{"date_experience":{"$gt":12}}, {"review_score":"5,0"}]}} ]))
print("{} documents with 'date_experience' > 12 months and 'review_score'==5,0".format(len(l)))
print()

# GET number of documents containing the word "experience" in its title or its comment 
import re
exp = re.compile(".*experience.*")
#l1 = list(mycol.find({  "$or":[ {'title':exp}, {"comment":exp} ]  }))
l2 = list(mycol.aggregate([ {"$match":{"$or":[{"title":exp}, {"comment":exp}]}} ]))
print("{} documents contain the word 'experience' either in its title or in its comment".format(len(l2)))
