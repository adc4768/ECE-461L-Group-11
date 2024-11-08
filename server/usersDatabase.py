# usersDatabase.py

from pymongo import MongoClient
import projectsDatabase as projectsDB

temp = 'User_DB'  # Replace with your actual database name

# Import encrypt and decrypt functions
def encrypt(inputText, N, D):
    reversedText = inputText[::-1]
    encryptedText = ""

    for c in reversedText:
        new_0 = chr(ord(c) + N * D)
        if 34 <= ord(new_0) <= 126:
            encryptedText += new_0
        else:
            new_1 = chr((ord(new_0) % 127) + 34)
            encryptedText += new_1
    return encryptedText

def decrypt(encryptedText, N, D):
    reversedText = encryptedText[::-1]
    decryptedText = ""

    for c in reversedText:
        new_0 = chr(ord(c) - N * D)
        if 34 <= ord(new_0) <= 126:
            decryptedText += new_0
        else:
            new_1 = chr((ord(new_0) % 127) + 34)
            decryptedText += new_1
    return decryptedText

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
    if __queryUser(client, username, userId) is not None:  # Check if the same user exists
        return False, 'User already exists.'
        
    # Encrypt the password
    N = 3
    D = 2
    encrypted_password = encrypt(password, N, D)
    
    # Create the user document
    User = {
        'username': username,
        'userId': userId,
        'password': encrypted_password,  # Store encrypted password
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

    # Decrypt the stored password
    encrypted_password = user['password']
    N = 3
    D = 2
    decrypted_password = decrypt(encrypted_password, N, D)

    # Compare the passwords
    if password == decrypted_password:
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
    if not result:
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
