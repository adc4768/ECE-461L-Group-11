# Import necessary libraries and modules
from pymongo import MongoClient

import projectsDatabase as projectsDB

temp = 'database_name' # After diciding the name of database, I gonna change here

'''
Structure of User entry:
User = {
    'username': username,
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

# Function to add a new user
def addUser(client, username, userId, password):
    if __queryUser(client, username, userId) is not None: # Check if the same use exists
        return False
        
    # Create the user document
    User = {
        'username': username,
        'userId': userId,
        'password': password,
        'projects': [] # Make Null projects
    }

    # Insert the user into the database
    db = client['temp']  
    users = db['users']
    result = users.insert_one(User)
    return result.inserted_id

# Helper function to query a user by username and userId
def __queryUser(client, username, userId):
    db = client[temp]
    users = db['users']
    user = users.find_one({'username': username, 'userId': userId})
    return user

# Function to log in a user
def login(client, username, userId, password):
    # Authenticate a user and return login status
    user = __queryUser(client, username, userId)
    if user is None:
        return False

    # Compare the hashed passwords
    if password == user['password']:
        return True
    else:
        return False


# Function to add a user to a project
def joinProject(client, userId, projectId):
    # Add a user to a specified project
    db = client[temp]  
    users = db['users']

    user = users.find_one({'userId': userId})
    if user is None:
        return False

    users.update_one(
        {'userId': userId},
        {'$addToSet': {'projects': projectId}}
    )

    result = projectsDB.addUser(client, projectId, userId)
    if result == 0:
        return False
    return True

# Function to get the list of projects for a user
def getUserProjectsList(client, userId):
    # Get and return the list of projects a user is part of
    db = client[temp]  
    users = db['users']

    user = users.find_one({'userId': userId})
    if user is None:
        return None
    return user.get('projects', [])
