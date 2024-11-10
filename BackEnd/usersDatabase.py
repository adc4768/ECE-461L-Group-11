from pymongo import MongoClient


temp = 'User_DB'  # Replace with your actual database name

# Encryption and decryption functions
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
    # Authenticate a user and return login status
    user = __queryUser(client, userId)
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
    
def join_project(client, userId, projectId):
    db = client['User_DB']
    projects = db['projects']
    users = db['users']

    #Check if the projectId exists or not
    existing_project = projects.find_one({'projectId': projectId})
    if existing_project:
        return False
    
        users = db['users']
    result = users.update_one(
        {'userId': userId},
        {'$addToSet': {'joiningPJ': projectId}}
    )

    if result.modified_count > 0:
        return True, 'Project successfully added to user joiningPJ.'
    else:
        return False, 'Project was already in joiningPJ or failed to add.'

