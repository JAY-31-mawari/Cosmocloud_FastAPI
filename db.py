from pymongo import MongoClient

MONGO_URL="mongodb+srv://sonu:jaymawari31@cluster0.ywepuzn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "python_api"
COLLECTION_NAME = "fastapi" 

client = MongoClient(MONGO_URL)
database = client[DATABASE_NAME]
collection = database[COLLECTION_NAME]
