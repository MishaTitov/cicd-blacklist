from pymongo import MongoClient
import os

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/") 
DATABASE_NAME = "blacklist"
COLLECTION_NAME = "entries"

def connect_to_mongodb():
    """
    Connect to MongoDB and return the collection object.
    """
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    return collection

def load_data():
    """
    Load all entries from MongoDB.
    """
    collection = connect_to_mongodb()
    entries = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB's _id field
    return entries

def add_entry(person_data):
    """
    Add a new entry to the MongoDB collection.
    """
    collection = connect_to_mongodb()
    collection.insert_one(person_data)

def delete_entry(name):
    """
    Delete an entry from the MongoDB collection by name.
    """
    collection = connect_to_mongodb()
    result = collection.delete_one({"name": name})
    return result.deleted_count > 0  # Return True if an entry was deleted

if __name__ == "__main__":
    # Test MongoDB connection
    collection = connect_to_mongodb()
    print("Connected to MongoDB!")