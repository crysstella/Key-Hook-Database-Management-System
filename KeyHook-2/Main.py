import string
from bson import DBRef
from pymongo.cursor import Cursor
from pymongo import ASCENDING
from src import Handling as Handling, Validator as Validator, Connect as Connect, DBCollections as DBCollections, Print
from pymongo.database import Database
from pymongo.collection import Collection

from src.PopulateData import PopulateData
from src.RequestStatus import RequestStatus
from src.UI import consoleUI


def delete():
    DBCollections.buildingType.delete_many({})
    DBCollections.room.delete_many({})
    DBCollections.doorName.delete_many({})
    DBCollections.door.delete_many({})
    DBCollections.hook.delete_many({})
    DBCollections.door_hook.delete_many({})
    DBCollections.keyCopy.delete_many({})
    DBCollections.employee.delete_many({})
    DBCollections.request.delete_many({})
    DBCollections.lossRequest.delete_many({})
    DBCollections.returnedRequest.delete_many({})


" Main function """
if __name__ == '__main__':
    # Connect to cluster
    db = Connect.data_connect()
    DBCollections.loadCollections(db)
    # delete()
    # PopulateData(db)
    consoleUI()











