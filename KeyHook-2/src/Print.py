import string

from src import DBCollections, Handling


def hooks_with_keys():
    # hooks: list = list()
    for hook in DBCollections.hook.find():
        hook_id = hook['id']
        print(f'Hook {hook_id}:')
        keys_obj: list = list(hook['key_copies'])  # list of key ObjectId
        if len(keys_obj) > 0:
            for key in keys_obj:
                key_id = DBCollections.keyCopy.find_one({'_id': key})['key_id']
                print(f'\tKey {key_id}')


def employees():
    for employee in DBCollections.employee.find():
        print(f'Employee {employee["id"]}: {employee["name"]}')


def buildings_rooms():
    for room in DBCollections.room.find():
        building = DBCollections.buildingType.find_one({'_id': room['building_type']})['type']
        print(f'Room {building} {room["number"]}')


def employees_rooms():
    for employee in DBCollections.employee.find():
        roomCanAccess(employee['id'])


def roomCanAccess(employee_id: int):
    employee = DBCollections.employee.find_one({'id': employee_id})
    employee_id = employee['id']
    employee_name = employee['name']
    print(f'Employee {employee_id}: {employee_name} can access to the rooms:')
    for req in DBCollections.request.find({'employee': employee['_id']}):
        room = DBCollections.room.find_one({'_id': req['room']})
        building = DBCollections.buildingType.find_one({'_id': room['building_type']})
        key_copy = DBCollections.keyCopy.find_one({'_id': req['key_copy']})
        hook = DBCollections.hook.find_one({'_id': key_copy['hook']})
        print(f'\t{building["type"]} {room["number"]} with: \t[key {key_copy["key_id"]}][hook {hook["id"]}]')


def availableKeys() -> list:
    # Keys in use
    used = list()
    availableKey = list()
    # cannot delete the key is in use
    for req in DBCollections.request.find():
        key_copy = DBCollections.keyCopy.find_one({'_id': req['key_copy']})
        used.append(key_copy['_id'])

    for hook in DBCollections.hook.find():
        hook_id = hook['id']
        print(f'Hook {hook_id}:')
        keys_obj: list = list(hook['key_copies'])  # list of key ObjectId
        if len(keys_obj) > 0:
            for key in keys_obj:
                if key not in used:
                    key_id = DBCollections.keyCopy.find_one({'_id': key})['key_id']
                    print(f'\tKey {key_id}')
                    availableKey.append(key_id)

    return availableKey


# def doorNames(hook_id: int):
#     hook = Handling.get_hook(hook_id)
#     doors: list = list(DBCollections.door_hook.find({'hook': hook['_id']}))
#     if doors is not None:
#         print(f'The hook {hook_id} can open the doors: ')
#         for door in doors:
#             room = DBCollections.room.find_one({'_id': door['room']})
#             door_name = DBCollections.door_name.find_one({'_id': door['location']})
#             building = DBCollections.buildingType.find_one({'_id': room['building_type']})
#             print(f'\t{building["type"]} {room["number"]} \t{door_name["location"]}')


def doorNames(type: string, room_number: int) -> int:
    # show exists door names in the room
    building = Handling.get_building_type(type)
    room = DBCollections.room.find_one({'number': room_number, 'building_type': building['_id']})
    print(f'{building["type"]} {room["number"]} exists door names: ')
    doors: list = list(room['doors'])
    if len(doors) == 0:
        print('Nothing in this room!')
    else:
        for door in doors:
            door_obj = DBCollections.door.find_one({'_id': door})
            location = DBCollections.doorName.find_one({'_id': door_obj['location']})
            print(f'\t{location["location"]}')
    return len(doors)



