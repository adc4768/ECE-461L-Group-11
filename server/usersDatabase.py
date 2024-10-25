# usersDatabase.py

from pymongo import MongoClient
import projectsDatabase as projectsDB
from werkzeug.security import generate_password_hash, check_password_hash

temp = 'User_DB'  # After deciding the name of the database, update here

'''
Structure of User entry:
User = {
    'username': username,
    'userId': userId,
    'password': password,  # Hashed password
    'projects': [project1_ID, project2_ID, ...]
}
'''

# Function to add a new user
def addUser(client, username, userId, password):
    if __queryUser(client, username, userId) is not None:  # Check if the same user exists
        return False, 'User already exists.'
        
    # Hash the password
    hashed_password = generate_password_hash(password)
    
    # Create the user document
    User = {
        'username': username,
        'userId': userId,
        'password': hashed_password,  # Store hashed password
        'projects': []  # Initialize with no projects
    }

    # Insert the user into the database
    db = client[temp]
    users = db['users']
    try:
        result = users.insert_one(User)
        if result.inserted_id:
            return True, 'User added successfully.'
        else:
            return False, 'Failed to add user.'
    except Exception as e:
        return False, f'Error: {str(e)}'

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
        return False, 'User not found.'

    # Verify the hashed password
    if check_password_hash(user['password'], password):
        return True, 'Login successful.'
    else:
        return False, 'Incorrect password.'

# Function to add a user to a project
def joinProject(client, userId, projectId):
    # Add a user to a specified project
    db = client[temp]  
    users = db['users']

    user = users.find_one({'userId': userId})
    if user is None:
        return False, 'User not found.'

    users.update_one(
        {'userId': userId},
        {'$addToSet': {'projects': projectId}}
    )

    result = projectsDB.addUser(client, projectId, userId)
    if result == 0:
        return False, 'Failed to add user to project.'
    return True, 'User added to project successfully.'

# Function to get the list of projects for a user
def getUserProjectsList(client, userId):
    # Get and return the list of projects a user is part of
    db = client[temp]  
    users = db['users']

    user = users.find_one({'userId': userId})
    if user is None:
        return False, 'User not found.'
    return True, user.get('projects', [])
