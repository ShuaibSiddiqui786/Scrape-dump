from pymongo import MongoClient

client = MongoClient("mongodb+srv://Anshika:anshika123@helenaai.usd8x.mongodb.net/")
db = client.test  # Test database
print(db.list_collection_names())  # This will list all collections in the 'test' database
