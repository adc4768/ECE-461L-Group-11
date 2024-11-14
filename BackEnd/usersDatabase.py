from pymongo import MongoClient
import logging



temp = 'User_DB'  # Replace with your actual database name

# Encryption and decryption functions
def encrypt(inputText, N, D):
    reversedText = inputText[::-1]
    encryptedText = ""

    for c in reversedText:
        new_0 = chr(ord(c) + N * D)
        if 32 <= ord(new_0) <= 126:
            encryptedText += new_0
        else:
            new_1 = chr(32 + (ord(new_0) - 32) % 95)
            encryptedText += new_1
    return encryptedText

def decrypt(encryptedText, N, D):
    reversedText = encryptedText[::-1]
    decryptedText = ""

    for c in reversedText:
        new_0 = chr(ord(c) - N * D)
        if 32 <= ord(new_0) <= 126:
            decryptedText += new_0
        else:
            new_1 = chr(32 + (ord(new_0) - 32) % 95)
            decryptedText += new_1
    return decryptedText








'''
Structure of User entry:
User = {
    'userId': userId,
    'password': password
    'joiningPJ' : []
}
'''

# Function to add a new user
def addUser(client, userId, password):
    if __queryUser(client, userId) is not None:  # Check if the same user exists
        return False, 'User already exists.'
        
    # Encrypt the password
    N = 3
    D = 2
    encrypted_password = encrypt(password, N, D)
    
    # Create the user document
    User = {
        'userId': userId,
        'password': encrypted_password , # Store encrypted password
        'joiningPJ' : []
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

# Helper function to query a user by userId
def __queryUser(client, userId):
    db = client[temp]
    users = db['users']
    user = users.find_one({'userId': userId})
    return user

# Function to log in a user
def login(client, userId, password):
    user = __queryUser(client, userId)
    if user is None:
        return False, 'User not found.'
    
    encrypted_password = user['password']
    decrypted_password = decrypt(encrypted_password, 3, 2)
    
    print(f"Decrypted Password: {decrypted_password}, Provided Password: {password}")
    
    if password == decrypted_password:
        return True, 'Login successful.'
    else:
        return False, 'Incorrect password.'


    
def join_project(client, userId, projectId):
    db = client['User_DB']
    projects = db['projects']
    users = db['users']

    existing_project = projects.find_one({'projectId': projectId})
    if not existing_project:
        logging.error('Project ID %s does not exist', projectId)
        return False, 'Project does not exist.'

    logging.info('Checking if project ID %s is already in user ID %s', projectId, userId)
    user = users.find_one({'userId': userId})

    if not user:
        logging.error('User ID %s does not exist', userId)
        return False, 'User does not exist.'
    
    if 'joiningPJ' not in user:
        logging.info('User ID %s does not have joiningPJ array, initializing it', userId)
        user['joiningPJ'] = []

    if projectId in user['joiningPJ']:
        logging.info('Project ID %s is already in the joiningPJ array of user ID %s', projectId, userId)
        return False, 'Project already added to user joiningPJ.'
    else:
        logging.info('Adding project ID %s to the joiningPJ array of user ID %s', projectId, userId)
        result = users.update_one(
            {'userId': userId},
            {'$addToSet': {'joiningPJ': projectId}}
        )
        if result.modified_count > 0:
            logging.info('Project ID %s successfully added to user ID %s', projectId, userId)
            return True, 'Project successfully added to user joiningPJ.'
        else:
            logging.error('Failed to add project ID %s to user ID %s for an unknown reason', projectId, userId)
            return False, 'Failed to add project to user joiningPJ.'
def get_evetyPRO_user_joining(client, userId):
    try:
        db = client[temp]
        users = db['users']
        
        # Query the user by userId
        user = users.find_one({'userId': userId})
        
        if user is None:
            return False, 'User not found.'
        
        # Retrieve the 'joiningPJ' list; return empty list if not present
        joining_projects = user.get('joiningPJ', [])
        
        return True, joining_projects
    
    except Exception as e:
        return False, f'An error occurred: {str(e)}'




