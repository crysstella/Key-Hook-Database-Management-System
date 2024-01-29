from src import Handling, Print


def consoleUI():
    finish = False
    # menu loop
    while finish is False:
        menuOptions()
        # userPrompt
        userInput: str = input()

        # add Key and display available hooks to use
        if userInput == 'a':
            a_done = False
            while not a_done:
                print('Current Keys: ')  # getHooks -> getKeys so users know if key exists or not
                Print.hooks_with_keys()
                try:
                    hook_id: int = int(input('Which hook will you pick? '))
                except ValueError:
                    print("That is not a valid integer")
                    continue
                key: dict = Handling.add_key(hook_id)
                if key is not None:
                    Print.hooks_with_keys()
                    a_done = True

        # addRequest
        if userInput == 'b':
            done = False
            while done is False:
                while True:
                    Print.employees()
                    employ_id_prompt: int = int(input('Enter an employee number: '))
                    employee = Handling.get_employee_by_id(employ_id_prompt)
                    if employee is None:
                        print('Employee not found!')
                    else:
                        break
                while True:
                    Print.buildings_rooms()
                    build_name_prompt = input('Enter a building name: ')
                    building = Handling.get_building_type(build_name_prompt)
                    if building is None:
                        print('Building not found!')
                    else:
                        break
                while True:
                    room_num_prompt: int = int(input('Enter a room number: '))
                    room = Handling.get_room(room_num_prompt, build_name_prompt)
                    if room is None:
                        print('Room not found!')
                    else:
                        done = True
                        request: dict = Handling.makeRequest(employ_id_prompt, build_name_prompt, room_num_prompt)
                        break

        # reportLoss / addLossRequest
        if userInput == 'c':
            print()
        # get all rooms an employee can enter with their key(s); needs to get all employees with keys (just iterate through requests for unique employees)
        if userInput == 'd':
            while True:
                Print.employees()
                employ_id_prompt: int = int(input('Enter an employee number: '))
                employee = Handling.get_employee_by_id(employ_id_prompt)
                if employee is None:
                    print('Employee not found!')
                else:
                    break
            Print.roomCanAccess(employ_id_prompt)

        # deleteKey and show all possible keys to delete
        if userInput == 'e':
            print('Available keys right now: ')
            keys = Print.availableKeys()
            while True:
                try:
                    key_id_prompt: int = int(input('Enter a key id to delete: '))
                except ValueError:
                    print("That is not a valid integer")
                    continue
                if key_id_prompt in keys:
                    Handling.deleteKey(key_id_prompt)
                    break
                else:
                    print('This key is not in the available keys')

        # deleteEmployee; must delete all requests related to them first; show all employees to delete in console
        if userInput == 'f':
            print()
        # addDoor based on existing hook; print all possible hooks and type desired one; name and and add door
        if userInput == 'g':
            Print.availableKeys()
            done = False
            while done is False:
                while True:
                    try:
                        hook_id: int = int(input('Which hook will you pick? '))
                    except ValueError:
                        print("That is not a valid integer")
                        continue
                    hook = Handling.get_hook(hook_id)
                    if hook is None:
                        print('Hook is not found!')
                    else:
                        break
                while True:
                    Print.buildings_rooms()
                    build_name_prompt = input('Enter a building name: ')
                    building = Handling.get_building_type(build_name_prompt)
                    if building is None:
                        print('Building not found!')
                    else:
                        break
                while True:
                    room_num_prompt: int = int(input('Enter a room number: '))
                    room = Handling.get_room(room_num_prompt, build_name_prompt)
                    if room is None:
                        print('Room not found!')
                    else:
                        door = Print.doorNames(build_name_prompt, room_num_prompt)
                        if door == 4:
                            print('The room is full. Cannot add new door to this room.')
                            break
                        else:
                            door_name = input('Enter a door name to add to this room: ')
                            door_name_check = Handling.get_door(door_name, room_num_prompt, build_name_prompt)
                            if door_name_check is None:
                                add_door = Handling.add_door(door_name, room_num_prompt, build_name_prompt)
                                if add_door is not None:
                                    Handling.add_door_hook(hook, add_door)
                                    print(f'Added [{door_name} {build_name_prompt} {room_num_prompt}] to [hook {hook_id}]')
                                    done = True
                                    break
                            else:
                                print('The door exists in the room. ')
        # updateRequest; if key is returned, make new request with new employee; if key is outgoing, then just swap employee associated
        if userInput == 'h':
            print()
        # find all employees who can get into a room; check all its doors and find the hook associated with it; take the hook and find all copies of it;
        # look for those copies based on current outgoing requests
        if userInput == 'i':
            print()
        # exits
        if userInput == 'j':
            finish = True


def menuOptions():
    # Menu Options
    print("Database UI:")
    print("Enter a to create a new key")
    print("Enter b to create a request with a given employee")
    print("Enter c to report a lost key")
    print("Enter d to report all the rooms an employee can enter with their current key")
    print("Enter e to delete a key")
    print("Enter f to delete an employee")
    print("Enter g to enter a new door that can be opened by an existing hook")
    print("Enter h to update an access request to move it to a new employee")
    print("Enter i to get a report on all employees who can get into a room")
    print("Enter j to exit")
