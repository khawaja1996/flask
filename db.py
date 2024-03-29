from flask_pymongo import PyMongo

mongo = PyMongo()

def initialize_db(app):
    mongo.init_app(app)

# Optionally, you can define some helper functions to interact with the database
def get_collection(collection_name):
    return mongo.db[collection_name]