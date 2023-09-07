### Objective:
- How to use SQLAlchemy to access a back-end database in PostgreSQL that is structured according to diagrams.
### Introduction:
- This project allows users to modify the tables according to the ***Diagrams*** folder.
- Populating some of the tables with data before running the application and only reading data from those tables.
- This application is written without any assumptions regarding the data already in the database. Pretend that multiple users could be running it at a time. Therefore, this project will accept input from the user and/or update the data in the database.
### Procedure:
- Take the ERD from Diagrams and execute tables.
- Populate some data for ***Employees, Buildings, rooms, doors, hooks***, and any junction tables between any two of those.
- A simple console interface provides a menu option for users to choose the way of modification:
  1.  Create a new Key.
  2.  Request access to a given room by a given employee.
  3.  Capture the issue of a key to an employee.
  4.  Capture losing a key.
  5.  Report out all the rooms that an employee can enter, given the keys that he/she already has.
  6.  Delete a key.
  7.  Delete an employee.
  8.  Add a new door that can be opened by an existing hook.
  9.  Update an access request to move it to a new employee.
  10.  Report out all the employees who can get into a room.

