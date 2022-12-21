"""This module contains a function to return a MongoDB client."""

from pymongo import MongoClient

def get_mongo_client() -> MongoClient:
    """returns a mongo client object"""
    username = 'root'
    password = '123abc'
    host = 'localhost'
    port = 27017
    return MongoClient(f'mongodb://{username}:{password}@{host}:{port}/')
