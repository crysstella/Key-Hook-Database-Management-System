from pymongo import MongoClient
from pymongo.database import Database
import os
from dotenv import load_dotenv
load_dotenv()


""" Connect to cluster
@return: a database object
@rtype: Database
"""


def data_connect() -> Database:
    cluster = f"mongodb+srv://{os.getenv('mongo_id')}:{os.getenv('mongo_pw')}@cecs-323.dcyfrka.mongodb.net" \
             f"/?retryWrites=true&w=majority"
    client = MongoClient(cluster)
    # client.drop_database('KeyHook')
    db = client['KeyHook']
    return db
