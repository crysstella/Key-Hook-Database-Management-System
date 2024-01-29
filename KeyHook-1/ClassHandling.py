from datetime import datetime

from DoorHook import DoorHook
from RequestStatus import RequestStatus
from BuildingType import BuildingType
from Door import Door
from DoorName import DoorName
from Employee import Employee
from Hook import Hook
from KeyCopy import KeyCopy
from LossRequest import LossRequest
from Request import Request
from ReturnedRequest import ReturnedRequest
from Room import Room
from main import Session
from sqlalchemy import exc, select


def getBuilding(name: str) -> BuildingType or None:
    """
    Checks for a match in the database and returns its Object.
    Since they can be uniquely identified this way, this method only returns one object.
    :param name: Building Name (Column: building_types.type)
    :return: Building if it exists, None otherwise.
    """
    with Session() as sess:
        statement = select(BuildingType).where(BuildingType.type == name)
        result = sess.execute(statement)
        for item in result.scalars():
            return item
    return None


def addBuilding(name: str) -> BuildingType or None:
    """
    Adds a building to the database if it does not exist.
    If the building already exists, return the building.
    This will return the first match.
    :param name: Building Name (Column: building_types.type)
    :return: Building if created or already exists, None if error thrown.
    """
    match = getBuilding(name)
    if match is not None:
        return match
    building = BuildingType(name)
    try:
        with Session() as sess:
            sess.add(building)
            sess.commit()
        return building
    except exc.SQLAlchemyError as error:
        print("Add Building Failed:", error)
        return None


def getRoom(building: str, number: int) -> Room or None:
    """
    Checks for a match in the database and returns its Object.
    Since they can be uniquely identified this way, this method only returns one object.
    :param building: Building Name (Column: building_types.type / rooms.building_type)
    :param number: Room Number (Column: rooms.number)
    :return: Room if it exists, None otherwise.
    """
    with Session() as sess:
        statement = select(Room).filter((Room.building_type == building) & (Room.number == number))
        result = sess.execute(statement)
        for item in result.scalars():
            return item
    return None


def getRooms(key: KeyCopy or int) -> [Room]:
    returnList = list()
    for door in getDoors(key):
        room: Room = getRoom(door.building_type, door.room_number)
        if room is not None:
            returnList.append(room)
    return returnList


def addRoom(building: BuildingType or str, number: int) -> Room or None:
    """
    Adds a room to the database if it does not exist.
    If the room already exists, return the room.
    This will return the first match.
    :param building: Building Name (Column: building_types.type / rooms.building_type)
    :param number: Room Number (Column: rooms.number)
    :return: Room if created or already exists, None if error thrown.
    """
    building: str = building.type if type(building) is BuildingType else building
    match = getRoom(building, number)
    if match is not None:
        return match
    room = Room(building, number)
    try:
        with Session() as sess:
            sess.add(room)
            sess.commit()
        return room
    except exc.SQLAlchemyError as error:
        print("Add Room Failed:", error)
        return None


def getDoorName(location: str) -> DoorName or None:
    with Session() as sess:
        statement = select(DoorName).filter((DoorName.location == location))
        result = sess.execute(statement)
        for item in result.scalars():
            return item
    return None


def addDoorName(location: str) -> DoorName or None:
    match = getDoorName(location)
    if match is not None:
        return match
    doorName = DoorName(location)
    try:
        with Session() as sess:
            sess.add(doorName)
            sess.commit()
        return doorName
    except exc.SQLAlchemyError as error:
        print("Add DoorName Failed:", error)
        return None


def getDoor(building: BuildingType or Room or str, number: Room or int, location: DoorName or str) -> Door or None:
    """
    Checks for a match in the database and returns its Object.
    Since they can be uniquely identified this way, this method only returns one object.
    :param building: Building Name (Column: building_types.type / rooms.building_type)
    :param number: Room Number (Column: rooms.number)
    :param location: Door Location (Column: door_name.location)
    :return: Room if it exists, None otherwise.
    """
    building: str = building.type if type(building) is BuildingType else building.building_type if type(building) is Room else building
    number: int = number.number if type(number) is Room else number
    location: str = location.location if type(location) is DoorName else location
    with Session() as sess:
        statement = select(Door).filter(
            (Door.location == location) & (Door.room_number == number) & (Door.building_type == building)
        )
        result = sess.execute(statement)
        for item in result.scalars():
            return item
    return None


def getDoors(key: KeyCopy or int) -> [Door]:
    key: KeyCopy = getKey(key) if type(key) is int else key
    if key is None:
        return list()
    hook: Hook = getHook(key.hooks_id)
    if hook is None:
        return list()
    returnList: [Door] = list()
    doorHook: DoorHook
    with Session() as sess:
        for doorHook in hook.door_list:
            statement = select(Door).filter((Door.id == doorHook.door_id))
            for door in sess.execute(statement).scalars():
                returnList.append(door)
    return returnList


def addDoor(building: BuildingType or Room or str, number: Room or int, location: DoorName or str) -> Door or None:
    match = getDoor(building, number, location)
    if match is not None:
        return match
    building: str = building.type if type(building) is BuildingType else building.building_type if type(building) is Room else building
    number: int = number.number if type(number) is Room else number
    location: str = location.location if type(location) is DoorName else location
    try:
        with Session() as sess:
            door = Door(building, number, location)
            sess.add(door)
            sess.commit()
            return door
    except exc.SQLAlchemyError as error:
        print("Add Door Failed:", error)
        return None


def getEmployees(name: str) -> [Employee]:
    returnList: [Employee] = list()
    with Session() as sess:
        statement = select(Employee).filter((Employee.name.contains(name)))
        result = sess.execute(statement)
        for item in result.scalars():
            returnList.append(item)
    return returnList


def addEmployee(name: str, force: bool = False) -> Employee or None:
    if not force:
        if len(getEmployees(name)) != 0:
            print("There are employees with this name, not adding...")
            return
    print("There are no employees with this name, adding...")
    employee: Employee = Employee(name)
    try:
        with Session() as sess:
            sess.add(employee)
            sess.commit()
        return employee
    except exc.SQLAlchemyError as error:
        print("Add Employee Failed:", error)
        return None


def getHook(hook_id: int) -> Hook or None:
    with Session() as sess:
        statement = select(Hook).filter((Hook.id == hook_id))
        result = sess.execute(statement)
        for item in result.scalars():
            return item
    return None


def addHook(hook_id: int, doors: [Door] = None) -> Hook or None:
    hook: Hook = getHook(hook_id)
    if hook is not None:
        with Session() as sess:
            for door in doors:
                hook.add_door(door)
            sess.commit()
        return hook
    with Session() as sess:
        hook = Hook(hook_id)
        sess.add(hook)
        for door in doors:
            hook.add_door(door)
        sess.commit()
    return hook


def getKey(key_id: int) -> KeyCopy or None:
    with Session() as sess:
        statement = select(KeyCopy).filter((KeyCopy.key_id == key_id))
        result = sess.execute(statement)
        for item in result.scalars():
            return item
    return None


def getKeys(hook: int or Hook) -> [KeyCopy]:
    returnList = list()
    hook: int = hook.id if type(hook) is Hook else hook
    with Session() as sess:
        statement = select(KeyCopy).filter((KeyCopy.hooks_id == hook))
        result = sess.execute(statement)
        for item in result.scalars():
            returnList.append(item)
    return returnList


def addKey(key_id: int, hook: Hook or int) -> KeyCopy or None:
    hook: int = hook.id if type(hook) is Hook else hook
    key: KeyCopy = getKey(key_id)
    if key is not None:
        print("Key already exists:", key)
        return key
    with Session() as sess:
        key = KeyCopy(key_id, hook)
        sess.add(key)
        sess.commit()
    return key


def getRequestStatus(request: Request or int) -> RequestStatus:
    request: int = request.requests_id if type(request) is Request else request
    with Session() as sess:
        request_statement = select(LossRequest).filter((LossRequest.requests_id == request))
        result = sess.execute(request_statement)
        for _ in result:
            return RequestStatus.LOST
        request_statement = select(ReturnedRequest).filter((ReturnedRequest.requests_id == request))
        result = sess.execute(request_statement)
        for _ in result:
            return RequestStatus.RETURNED
        return RequestStatus.OUT


def makeRequest(employee: int or Employee, building: BuildingType or Room or str, room_number: Room or int) -> Request or None:
    # Normalize inputs
    employee: int = employee.id if type(employee) is Employee else employee
    building: str = building.type if type(building) is BuildingType else building.building_type if type(building) is Room else building
    room_number: int = room_number.number if type(room_number) is Room else room_number

    # See what keys can open the room.
    with Session() as sess:
        doors_statement = select(Door).filter((Door.room_number == room_number) & (Door.building_type == building))
        doors_result = sess.execute(doors_statement)
        door: Door
        all_requests: [Request] = list()
        valid_keys: [KeyCopy] = list()
        # Door -> DoorHook -> Hook -> Key
        for door in doors_result.scalars():
            doorHook: DoorHook
            for doorHook in door.hook_list:
                key: KeyCopy
                for key in doorHook.hook.keys:
                    valid_keys.append(key)
                    requests_statement = select(Request).filter((Request.key_id == key.key_id))
                    for item in sess.execute(requests_statement).scalars():
                        all_requests.append(item)

        # Remove unavailable keys.
        for request in all_requests:
            status: RequestStatus = getRequestStatus(request)
            if status == RequestStatus.LOST or status == RequestStatus.OUT:
                key_statement = select(KeyCopy).filter((KeyCopy.key_id == request.key_id))
                for item in sess.execute(key_statement).scalars():
                    try:
                        valid_keys.remove(item)
                    except ValueError as e:
                        print(f"ERROR: {e}\n\t{item} is not in {valid_keys}")

        # Determine if there are any keys left.
        if len(valid_keys) == 0:
            print("Request cannot be made, there are no keys available right now!")
            return None

        # Determine if the employee already has a key that opens the door.
        open_statement = select(Request).filter((Request.building_type == building) & (Request.rooms_number == room_number) & (Request.employees_id == employee))
        item: Request
        for item in sess.execute(open_statement).scalars():
            if getRequestStatus(item) == RequestStatus.OUT:
                print(f"Request cannot be made, Employee #{item.employees_id} already has access to {item.building_type} {item.rooms_number} with key {item.key_id} borrowed on {item.borrow_date}")
                return None

        # Assign a key and datetime
        key: KeyCopy = valid_keys[0]
        dateTime: datetime = datetime.now()
        request: Request = Request(dateTime, employee, room_number, building, key.key_id)
        sess.add(request)
        sess.commit()
        sess.close()
        # Return request
        return request


def updateStatus(request: Request or int, status: RequestStatus) -> LossRequest or ReturnedRequest or None:
    if status == RequestStatus.OUT:
        print(f"Unsupported! Cannot update {request} to be {status}")
        return None

    request: int = request.requests_id if type(request) is Request else request
    with Session() as sess:
        statement = select(Request).filter((Request.requests_id == request))
        request_item: Request
        for request_item in sess.execute(statement).scalars():
            request_status: RequestStatus = getRequestStatus(request_item)
            if request_status == RequestStatus.OUT:
                if status == RequestStatus.LOST:
                    loss: LossRequest = LossRequest(request_item.requests_id, datetime.now())
                    sess.add(loss)
                    sess.commit()
                    return loss
                if status == RequestStatus.RETURNED:
                    returned: ReturnedRequest = ReturnedRequest(request_item.requests_id, datetime.now())
                    sess.add(returned)
                    sess.commit()
                    return returned
            print(f"{request_item} has a status of {request_status}")


def getRequests(employee: Employee or int) -> [Request]:
    employee: int = employee.id if type(employee) is Employee else employee
    returnList: [Request] = list()
    with Session() as sess:
        statement = select(Request).filter((Request.employees_id == employee))
        for item in sess.execute(statement).scalars():
            returnList.append(item)
    return returnList
