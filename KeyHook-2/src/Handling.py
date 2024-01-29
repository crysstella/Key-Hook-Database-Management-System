from datetime import datetime
import string

from bson import ObjectId
from pymongo.cursor import Cursor

from src.RequestStatus import RequestStatus
from pymongo.results import InsertOneResult
from pymongo.collection import Collection
from src import DBCollections as DBCollections

key_id = 0
request_id = 0


def add_building_type(type: string) -> dict:
    match = get_building_type(type)
    if match is not None:
        print(f'[{type}] is already in [building_types]')
        return match
    result: InsertOneResult = DBCollections.buildingType.insert_one({'type': type, 'rooms': []})
    print(f'[{type}] is added to [building_types]')
    return DBCollections.buildingType.find_one({'_id': result.inserted_id})


def get_building_type(type: string) -> dict:
    find = DBCollections.buildingType.find_one({'type': type})
    return find


def add_room(number: int, type: string) -> dict:
    match = get_room(number, type)
    if match is not None:
        print(f'[{type} {number}] is already in [rooms]')
        return match
    type_dict: dict = add_building_type(type)
    if type_dict is None:
        return None
    # result: InsertOneResult = DBCollections.room.insert_one(
    #     {'number': number, 'building_type': DBRef('building_types', type_dict['_id'])})
    result: InsertOneResult = DBCollections.room.insert_one(
        {'number': number, 'building_type': type_dict['_id'], 'doors': [], 'requests': []})
    room_dict = DBCollections.room.find_one({'_id': result.inserted_id})
    print(f'[{type} {number}] is added to [rooms]')
    DBCollections.buildingType.update_one({'_id': type_dict['_id']},
                                          {'$push': {'rooms': room_dict['_id']}})
    return room_dict


def get_room(number: int, type: string) -> dict:
    type_dict = get_building_type(type)
    if type_dict is None:
        return None
    room_find = {'number': number, 'building_type': type_dict['_id']}
    find = DBCollections.room.find_one(room_find)
    return find


def add_door_name(location: string) -> dict:
    try:
        match = get_door_name(location)
        if match is not None:
            print(f'[{location}] is already in [door_names]')
            return match
        result: InsertOneResult = DBCollections.doorName.insert_one({'location': location, 'doors': []})
        print(f'[{location}] is added to [door_names]')
        return DBCollections.doorName.find_one({'_id': result.inserted_id})
    except Exception as E:
        print(f'Invalid door name: [{location}]')
        return None


def get_door_name(location: string) -> dict:
    find = DBCollections.doorName.find_one({'location': location})
    return find


def add_door(location: string, room_number: int, type: string) -> dict:
    try:
        match = get_door(location, room_number, type)
        if match is not None:
            print(f'[{location}] is already in [{type} {room_number}]')
            return match
        door_name_dict: dict = get_door_name(location)
        room_dict: dict = get_room(room_number, type)
        building_type_dict = get_building_type(type)
        if door_name_dict is None or room_dict is None or building_type_dict is None:
            print(
                f'[{location} {type} {room_number}] - One of the door name, room, or building type is not in the database')
            return None
        result: InsertOneResult = DBCollections.door.insert_one({'location': door_name_dict['_id'],
                                                                 'room': room_dict['_id']})
        door_dict = DBCollections.door.find_one({'_id': result.inserted_id})
        DBCollections.room.update_one({'_id': room_dict['_id']},
                                      {'$push': {'doors': door_dict['_id']}})
        DBCollections.doorName.update_one({'_id': door_name_dict['_id']},
                                          {'$push': {'doors': door_dict['_id']}})
        print(f'[{location} {type} {room_number}] is added to [doors]')
        return door_dict
    except Exception as E:
        print(f'Invalid door: [{location} {type} {room_number}]')
        print(E)


def get_door(location: string, room_number: int, type: string) -> dict:
    door_dict = get_door_name(location)
    room_dict = get_room(room_number, type)
    building_type_dict = get_building_type(type)
    if door_dict is None or room_dict is None or building_type_dict is None:
        return None
    door_find = {'location': door_dict['_id'], 'room': room_dict['_id']}
    find = DBCollections.door.find_one(door_find)
    return find


def add_hook(id: int) -> dict:
    match = get_hook(id)
    if match is not None:
        print(f'[hook {id}] is already in [hooks]')
        return match
    result: InsertOneResult = DBCollections.hook.insert_one({'id': id, 'key_copies': []})
    print(f'[hook {id}] is added to [hooks]')
    return DBCollections.hook.find_one({'_id': result.inserted_id})


def get_hook(id: int) -> dict:
    find = DBCollections.hook.find_one({'id': id})
    return find


def add_key(hook_id: int) -> dict:
    global key_id
    hook_dict = get_hook(hook_id)
    if hook_dict is None:
        print(f'[hook {hook_id}] is not in [hooks]')
        return None
    # hook_dict: dict = get_hook(hook_id)
    key_id += 1
    result: InsertOneResult = DBCollections.keyCopy.insert_one(
        {'key_id': key_id, 'hook': hook_dict['_id'], 'requests': []})
    print(f'[key {key_id}][hook {hook_id}] is added to [keys]')
    DBCollections.hook.update_one({'_id': hook_dict['_id']},
                                  {'$push': {'key_copies': result.inserted_id}})
    return DBCollections.keyCopy.find_one({'_id': result.inserted_id})


def add_door_hook(hook: dict, door: dict):
    DBCollections.door_hook.insert_one(
        {
            'hook': hook['_id'],
            'door': door['_id']
        }
    )


def get_key(hook_id: int) -> dict:
    hook = get_hook(hook_id)
    find = DBCollections.keyCopy.find_one({'key_id': key_id, 'hook': hook['_id']})
    return find


def add_employee(id: int, name: string) -> dict:
    try:
        match = get_employee(id, name)
        if match is not None:
            return match
        result: InsertOneResult = DBCollections.employee.insert_one({'id': id, 'name': name, 'requests': []})
        print(f'employee[{id}][{name}] is added to [employees]')
        return DBCollections.employee.find({'_id': result.inserted_id})
    except Exception as E:
        print(E)


def get_employee(id: int, name: string) -> dict:
    find = DBCollections.employee.find_one({'id': id, 'name': name})
    return find


def get_employee_by_id(id: int) -> dict:
    find = DBCollections.employee.find_one({'id': id})
    return find


def getRequestStatus(id: int) -> RequestStatus:
    request: dict = DBCollections.request.find_one({'request_id': id})
    loss: dict = DBCollections.lossRequest.find_one({'request': request['_id']})
    if loss is not None:
        return RequestStatus.LOST
    returned: dict = DBCollections.returnedRequest.find_one({'request': request['_id']})
    if returned is not None:
        return RequestStatus.RETURNED
    return RequestStatus.OUT


def makeRequest(employee_id, type: string, room_number: int) -> dict:
    # What keys can open the room
    building: dict = get_building_type(type)
    room: dict = get_room(room_number, building['type'])
    doors: list = list(DBCollections.door.find({'room': room['_id']}))

    # door -> dook_hook -> hook -> key
    valid_keys: list = []
    all_request: list = []
    for d in doors:
        hooks: list = list(DBCollections.door_hook.find({'door': d['_id']}))
        for h in hooks:
            hook: dict = DBCollections.hook.find_one({'_id': h['hook']})
            key_copies: list = list(hook['key_copies'])
            for k in key_copies:
                valid_keys.append(k)
                request: dict = DBCollections.request.find_one({'key_copy': k})
                if request is not None:
                    all_request.append(request)

    # Remove unavailable keys
    for req in all_request:
        status: RequestStatus = getRequestStatus(req['request_id'])
        if status == RequestStatus.LOST or status == RequestStatus.OUT:
            valid_keys = [k for k in valid_keys if k != req['key_copy']]

    # Determine if there are any keys left
    if len(valid_keys) == 0:
        print('No keys available')
        return None

    # Determine if the employee already has a key that opens the door.
    target: dict = room
    for door in getDoorsFromEmployee(employee_id):
        if door['room'] == target['_id']:
            print("Cannot make a new request, this person already has access to this room!")
            return None

    # Assign a key and datetime
    global request_id
    request_id += 1
    key: string = valid_keys[0]
    borrow_date: datetime = datetime.now()
    employee: dict = DBCollections.employee.find_one({'id': employee_id})
    result: InsertOneResult = DBCollections.request.insert_one(
        {'request_id': request_id, 'borrow_date': borrow_date, 'employee': employee['_id'], 'room': room['_id'], 'key_copy': key})
    DBCollections.employee.update_one({'_id': employee['_id']}, {'$push': {'requests': result.inserted_id}})
    DBCollections.keyCopy.update_one({'_id': key}, {'$push': {'requests': result.inserted_id}})
    DBCollections.room.update_one({'_id': room['_id']}, {'$push': {'requests': result.inserted_id}})
    key_copy: dict = DBCollections.keyCopy.find_one({'_id': key})
    print(
        f"Request {request_id} made for Employee #{employee['id']} to access {building['type']} {room['number']} with key {key_copy['key_id']}")
    return DBCollections.request.find_one({'_id': result.inserted_id})


def updateStatus(id: int, status: RequestStatus) -> dict:
    if status == RequestStatus.OUT:
        print(f"Unsupported! Cannot update {id} to be {status}")
        return None
    request: dict = DBCollections.request.find_one({'request_id': id})
    if request is None:
        return None
    request_status = getRequestStatus(id)
    if request_status == RequestStatus.OUT:
        if status == RequestStatus.LOST:
            result: InsertOneResult = DBCollections.lossRequest.insert_one({'request': request['_id'],
                                                                            'loss_date': datetime.now()})
        if status == RequestStatus.RETURNED:
            result: InsertOneResult = DBCollections.returnedRequest.insert_one({'request': request['_id'],
                                                                                'return_date': datetime.now()})
        print(f"Request {request['request_id']} is now {status}")
        return DBCollections.request.find_one({'_id': result.inserted_id})


def getDoorsFromEmployee(employee_id: int) -> [dict]:
    requestList: [dict] = list()
    hookList: [dict] = list()
    doorList: [dict] = list()
    employee: dict = DBCollections.employee.find_one({"id": employee_id})

    for doc in DBCollections.request.find({"employee": employee["_id"]}):
        if getRequestStatus(doc["request_id"]) == RequestStatus.OUT:
            requestList.append(doc)

    for request in requestList:
        key: dict = DBCollections.keyCopy.find_one({"_id": request["key_copy"]})
        if key is None:
            continue
        hookList.append(DBCollections.hook.find_one({'_id': key['hook']}))

    for hook in hookList:
        for door_hook in DBCollections.door_hook.find({'hook': hook['_id']}):
            doorList.append(DBCollections.door.find_one({"_id": door_hook['door']}))

    return doorList


def deleteKey(id: int):
    key = DBCollections.keyCopy.find_one({'key_id': id})
    # delete it from hook
    hook = DBCollections.hook.find_one({'_id': key['hook']})
    keys: list = list(hook['key_copies'])
    if key['_id'] in keys:
        DBCollections.hook.update_one({'_id': hook['_id']}, {'$pull': {'key_copies': key['_id']}})
    request = DBCollections.request.find({'key_copy': key['_id']})
    if request is not None:
        for req in request:
            DBCollections.request.delete_one({'_id': req['_id']})
    DBCollections.keyCopy.delete_one({'_id': key['_id']})

    print(f'Key {key["key_id"]} deleted.')


def getAvailableDoorName(type: string, room_number: int) -> string:
    building = get_building_type(type)
    room = DBCollections.room.find_one({'number': room_number, 'building_type': building['_id']})
    doors: list = list(room['doors'])
    for door in doors:
        door_obj = DBCollections.door.find_one({'_id': door})
        location = DBCollections.doorName.find_one({'_id': door_obj['location']})