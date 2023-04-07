[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-8d59dc4de5201274e310e4c54b9627a8934c3b88527886e3b421487c677d23eb.svg)](https://classroom.github.com/a/x4M2JGGT)
# Pset 3: Web Application (Version 1)

### Due Friday April 7 11:59 PM NHT (New Haven Time)

### CPSC 419 PSET 2 PARTNER GROUP 9

Group members: Sophia Kang (yk575), Phuc Duong (phd24), both enrolled in CPSC 419.

### Contributions
Sophia Kang contribution:
- Writing Jinja statements in index.html
- Writing HTML for error.html, index.html, luxdetails.html
- Creating /search and /obj/<object_id> routes and adding functionality to search database and parse/return data to the html file.
- Error Handling: Bad Server, Bad Client, Invalid Search Parameters, Missing "obj_id" and adding the error pages
- Saving and loading cookies to enable user to go back to previous searches and have the form filled with the information that they had before.

Phuc Duong contribution:
- Setting up runserver.py
- Writing HTML for index.html
- Added CSS styling for table and form-field
- Creating /search and /obj/<object_id> routes and adding functionality to search database and parse/return data to the html file.
- Error Handling: Catching exception for unable to open data base
- Saving and loading cookies to enable user to go back to previous searches and have the form filled with the information that they had before.

### Pylint information to graders
- luxapp.py: We are getting "Access to a protected member _exit of a client class" which is the result of using the os._exit function to exit out of our Flask application if there is a sqlite3 OperationalError with the given database filename. Using sys.exit(1) does not work in this case, so this was an unavoidable pylint error.
- query.py: we have a pylint error that says too many local variables, but we only exceeded the limit by 4 and have tried to eliminate local variables without making the code unreadable. There is an error with the number of arguments from LuxDetailsQuery, because we inherit from the Query class, but we think this is negligible for the most part. 
- runserver.py: We get 2 broad-exception-caught errors. However, this is extended behavior as we are trying to exit the program safely we want to try to catch a general exception just in case. We have specific exception already where neccessary.