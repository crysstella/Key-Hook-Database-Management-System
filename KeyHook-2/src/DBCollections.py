from pymongo.collection import Collection
from pymongo.database import Database

buildingType: Collection or None = None
room: Collection or None = None
doorName: Collection or None = None
door: Collection or None = None
hook: Collection or None = None
door_hook: Collection or None = None
keyCopy: Collection or None = None
employee: Collection or None = None
request: Collection or None = None
lossRequest: Collection or None = None
returnedRequest: Collection or None = None


def loadCollections(db: Database):
    global buildingType
    global room
    global doorName
    global door
    global hook
    global door_hook
    global keyCopy
    global employee
    global request
    global lossRequest
    global returnedRequest

    buildingType = db['building_types']
    room = db['rooms']
    doorName = db['door_names']
    door = db['doors']
    hook = db['hooks']
    door_hook = db['door_hook']
    keyCopy = db['key_copies']
    employee = db['employees']
    request = db['requests']
    lossRequest = db['loss_requests']
    returnedRequest = db['returned_requests']

