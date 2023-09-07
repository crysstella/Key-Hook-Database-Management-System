### Objective: 
- How to use MongoDB to serialize data that is structured according to ***Diagrams*** folder.
### Introduction:
- To improve the time to update all the classes from the tables by using MongoDB.
- Populate seed data before running the application.
### Notice:
In main.py:
1. Populate the data to MongoDB by `PopulateData(db)`
2. Once your program stops running, you should comment out:
   - `PopulateData(db)` function to not put more data in MongoDB.
   - `delete()` function to save the data in MongoDB.
3. Run `main.py` to get the result.
### Procedure:
1. Implement the relationships between tables by Mongo tools:
 - Uniqueness constraints.
 - References (to simulate relationships).
 - MongoDB schemas on your collections.
2. Populate seed data for ***Employees, Buildings, rooms, doors, hooks,*** and any junction collections between any two of those.
3. Creating a simple console interface to:
   - Create a new Key.
     - Present the user with a list of the available hooks.
     - Prompt them for which hook they will use to make the key.
     - Generate the key number.  I prefer that you use a serial for that.
   - Request access to a given room by a given employee.
     - Present the user with a list of the Employees by name and prompt for which one.
     - Present the user with a list of the buildings and rooms and prompt for which one – note: you can do that as one prompt if you really want to.
   - Capture the issue of a key to an employee.
     - This could be part of giving access if you structured your data that way.
     - Prompt them for the Access.
     - Then you either find the existing key that meets that need, or you make a new one on a hook of your choice that opens at least one of the doors to that room.
   - Capture losing a key.
     - Prompt them for the key request that was lost.
     - Capture the date and time of the loss.  You can default to the current date and time. 
   - Report out all the rooms that an employee can enter, given the keys that he/she already has.
     - Prompt for the employee.
     - List the rooms that they have access to:
       - Order by building, then room.
       - Remove duplicates.
   - Delete a key.
     - Check for any references to that key.
       - Either delete the references first.
       - Or put it into a try/catch block and let the user know that the key is in use and you cannot delete it.
     - Only delete the key if it will not cause an exception to show on the screen.
   - Delete an employee.
     - Same basic cautions as deleting a key.
   - Add a new door that can be opened by an existing hook.
     - Prompt them for the hook.
     - Prompt them for the building.
     - Prompt them for the room.
     - Provide a menu of the available door names and prompt for which door they want.
   -	Update an access request to move it to a new employee.
     - Prompt for the old employee.
     - Prompt for which access (by room) of theirs that you’re to move.
   - Report out all the employees who can get into a room.
     - Prompt for the room.
     - List the employees by name.

