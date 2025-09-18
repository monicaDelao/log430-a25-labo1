
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from models.user import User

class UserDAOMongo:
    def __init__(self):
        env_path = find_dotenv()
        load_dotenv(dotenv_path=env_path)
        host = os.getenv("MONGODB_HOST", "localhost")
        port = int(os.getenv("MONGODB_PORT", 27017))
        db_name = os.getenv("MONGODB_DATABASE", "store_db")

        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db["users"]

    def select_all(self):
        users = []
        for doc in self.collection.find():
            user = User(id=str(doc["_id"]), name=doc["name"], email=doc["email"])
            users.append(user)
        return users

    def insert(self, user):
        doc = {"name": user.name, "email": user.email}
        result = self.collection.insert_one(doc)
        user.id = str(result.inserted_id)
        return user.id 

    def update(self, user):
        self.collection.update_one(
            {"_id": ObjectId(user.id)},
            {"$set": {"name": user.name, "email": user.email}}
        )

    def delete(self, user_id):
        self.collection.delete_one({"_id": ObjectId(user_id)})

    def delete_all(self):
        self.collection.delete_many({})
