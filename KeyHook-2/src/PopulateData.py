from pymongo import ASCENDING
from pymongo.database import Database

from src import Handling as Handling, Validator as Validator, Connect as Connect, DBCollections as DBCollections


def PopulateData(db: Database):
    # db.create_collection('door_hook')
    # db.create_collection('loss_requests')
    # db.create_collection('returned_requests')

    DBCollections.buildingType.create_index([('type', ASCENDING)], unique=True)
    buildingType_validator = Validator.building_type_validator()
    db.command('collMod', 'building_types', **buildingType_validator)

    Handling.add_building_type('CECS')
    Handling.add_building_type('ENGR')

    DBCollections.room.create_index([('number', ASCENDING),
                                     ('building_type', ASCENDING)], unique=True)
    room_validator = Validator.room_validator()
    db.command('collMod', 'rooms', **room_validator)

    Handling.add_room(323, 'CECS')
    Handling.add_room(303, 'CECS')
    Handling.add_room(305, 'ENGR')
    Handling.add_room(493, 'MUSC')

    DBCollections.doorName.create_index([('location', ASCENDING)], unique=True)
    doorName_validator = Validator.door_name_validator()
    db.command('collMod', 'door_names', **doorName_validator)

    Handling.add_door_name('south')
    Handling.add_door_name('east')
    Handling.add_door_name('west')
    Handling.add_door_name('north')
    Handling.add_door_name('eastwest')
    Handling.add_door_name('south')

    DBCollections.door.create_index([('location', ASCENDING),
                                     ('room', ASCENDING)], unique=True)
    door_validator = Validator.door_validator()
    db.command('collMod', 'doors', **door_validator)

    # Handling.add_door('south', 323, 'CECS')  # duplicate
    # Handling.add_door('south', 303, 'CECS')  # 303 is not in building type CECS
    door_list = [Handling.add_door('south', 323, 'CECS'), Handling.add_door('north', 323, 'CECS'),
                 Handling.add_door('west', 323, 'CECS'), Handling.add_door('east', 323, 'CECS'),
                 Handling.add_door('east', 305, 'ENGR'), Handling.add_door('north', 305, 'ENGR'),
                 Handling.add_door('east', 493, 'MUSC'), Handling.add_door('west', 493, 'MUSC')]

    DBCollections.hook.create_index([('id', ASCENDING)], unique=True)
    hook_validator = Validator.hook_validator()
    db.command('collMod', 'hooks', **hook_validator)

    hook_list = [Handling.add_hook(1), Handling.add_hook(2),
                 Handling.add_hook(3), Handling.add_hook(4),
                 Handling.add_hook(5), Handling.add_hook(6)]

    door_hook_validator = Validator.door_hook_validator()
    db.command('collMod', 'door_hook', **door_hook_validator)

    Handling.add_door_hook(hook_list[1], door_list[0])
    Handling.add_door_hook(hook_list[2], door_list[0])
    Handling.add_door_hook(hook_list[3], door_list[0])
    Handling.add_door_hook(hook_list[4], door_list[0])
    Handling.add_door_hook(hook_list[5], door_list[0])
    Handling.add_door_hook(hook_list[1], door_list[4])

    DBCollections.keyCopy.create_index([('key_id', ASCENDING)], unique=True)
    keyCopy_validator = Validator.key_copy_validator()
    db.command('collMod', 'key_copies', **keyCopy_validator)

    # add_key(hook_id)
    Handling.add_key(2)
    Handling.add_key(2)
    Handling.add_key(2)
    Handling.add_key(2)
    Handling.add_key(2)
    Handling.add_key(4)
    Handling.add_key(6)

    DBCollections.employee.create_index([('id', ASCENDING)], unique=True)
    employee_validator = Validator.employee_validator()
    db.command('collMod', 'employees', **employee_validator)

    Handling.add_employee(1, 'Stellar Nguyen')
    Handling.add_employee(2, 'Stellar Le')
    Handling.add_employee(3, 'Nick Le')
    Handling.add_employee(4, 'Nilar Le')
    Handling.add_employee(5, 'Jared Siville')
    Handling.add_employee(6, 'Paul Nguyen')

    DBCollections.request.create_index([('request_id', ASCENDING)], unique=True)
    request_validator = Validator.request_validator()
    db.command('collMod', 'requests', **request_validator)

    Handling.makeRequest(1, 'CECS', 323)
    Handling.makeRequest(1, 'CECS', 323)
    Handling.makeRequest(2, 'CECS', 323)
    Handling.makeRequest(3, 'CECS', 323)
    Handling.makeRequest(4, 'ENGR', 305)
    Handling.makeRequest(4, 'MUSC', 493)

    DBCollections.lossRequest.create_index([('request', ASCENDING)], unique=True)
    loss_request_validator = Validator.loss_request_validator()
    db.command('collMod', 'loss_requests', **loss_request_validator)

    # updateStatus(request_id: int, status: RequestStatus)
    DBCollections.returnedRequest.create_index([('request', ASCENDING)], unique=True)
    return_request_validator = Validator.returned_request_validator()
    db.command('collMod', 'returned_requests', **return_request_validator)

