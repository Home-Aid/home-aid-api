import logging
from pymongo import MongoClient
import os
# from utils.constants import DATABASE, USER_DB
from src.utils.constants import DATABASE, USER_DB
from env.envConfig import env
from src.utils.logging import logger



# MONGODB_URI = os.getenv("MONGODB_URL", "")
MONGODB_URL = "mongodb+srv://{}:{}@logistics.pyposnp.mongodb.net/?retryWrites=true&w=majority&appName=Logistics"
MONGODB_URI = MONGODB_URL.format(env.get("USERNAME"), env.get("PASSWORD"))


class MongoDB:
    """
    MongoDB class to interact with MongoDB database.
    """

    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE]


# Initialize MongoDB
db = MongoDB().db


class MongoService:
    @staticmethod
    def fetch(collection, query=None, projection=None, limit=0, skip=0, sort=None, fetch_all=False):
        """
        Description: Fetch data from MongoDB
        Args:
            collection: Collection name in MongoDB
            query: Query to filter data | {"key": "value"}
            projection: Fields to include/exclude | {"key": 1, "_id": 0}
            limit: Number of records to fetch 
            skip: Number of records to skip
            sort: Sort data | [("key", 1)] for ascending, [("key", -1)] for descending
            fetch_all: True to fetch all records, False to fetch one record
        """
        projection = {"_id": 0} if not projection else {"_id": 0, **projection}
        if fetch_all:
            cursor = db[collection].find(query, projection)
            if sort:
                cursor = cursor.sort(sort)
            if limit:
                cursor = cursor.limit(limit).skip(skip)

            return list(cursor)
        else:
            return db[collection].find_one(query, projection)

    def count(collection, query=None):
        """
        Description: Count data from MongoDB
        Args:
            collection: Collection name in MongoDB
            query: Query to filter data | {"key": "value"}
        """
        return db[collection].count_documents(query or {})

    @staticmethod
    def insert(collection, data, many=False):
        """
        Description: Insert data into MongoDB
        Args:
            collection: Collection name in MongoDB
            data: Data to insert | {"key": "value"} for single record, [{"key": "value"}] for multiple records
            many: True to insert multiple records, False to insert single record
        """
        if many:
            inserted_ids = db[collection].insert_many(data).inserted_ids
            # [ObjectId('66819575c056155dd5cd4417'), ObjectId('66819575c056155dd5cd4418')]
            return [str(id) for id in inserted_ids]
        else:
            return db[collection].insert_one(data).inserted_id

    @staticmethod
    def update(collection, query, data):
        """
        Description: Update data in MongoDB
        Args:
            collection: Collection name in MongoDB
            query: Query to filter data | {"key": "value"}
            data: Data to update | {"$set": {"key": "value"}}
            many: True to update multiple records, False to update single record
        """
        return db[collection].update_many(query, data)


# Test count
# query = {"name": "gaurav"}
# result = MongoService.count(USER_DB, query)
# print(f"\n\n Result: {result}")

# Test update data
# query = {"name": "gaurav"}
# data = {"$set": {"data": 123456}}
# result = MongoService.update(USER_DB, query, data)
# print(f"\n\n Result: {result}")

# Example usage
# query = {"name": "gaurav"}
# projection = {"_id": 0}
# sort = [("mobile", -1)]
# result = MongoService.fetch(USER_DB, query=query, projection=projection, sort=sort, fetch_all=True)

# Check insertetd data
# data = {
#     "name": "pqr",
#     "email": "pqr@gmail.com",
#     "mobile": 12
# }

# data = MongoService.insert(USER_DB, data)
# print(f"\n\n Data: {data}")

# Check multiple data insert

# data = [
#    {
#     "name": "abc1",
#     "email": "ab1c@gmail.com",
#     "mobile": 22,
# },
# {
#     "name": "xyz1",
#     "email": "xyz1@gmail.com",
#     "mobile": 33,
# }
# ]

# data = MongoService.insert(USER_DB, data, many=True)

# print(f"data: {data}")
