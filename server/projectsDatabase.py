# projectsDatabase.py

# Import necessary libraries and modules
from pymongo import MongoClient
import hardwareDatabase as HardwareDB

'''
Structure of Project entry:
Project = {
    'projectName': projectName,
    'projectId': projectId,
    'description': description,
    'hwSets': {HW1: qty1, HW2: qty2, ...},
    'users': [user1, user2, ...]
}
'''

# Function to query a project by its ID
def queryProject(client, projectId):
    db = client['User_DB']
    projects = db['projects']
    
    project = projects.find_one({'projectId': projectId})
    
    return project

# Function to create a new project
def createProject(client, projectName, projectId, description):
    db = client['User_DB']
    projects = db['projects']
    
    # Check if the project already exists
    existing_project = projects.find_one({'projectId': projectId})
    if existing_project:
        return False  # Project already exists
    
    # Create the project document
    project = {
        'projectName': projectName,
        'projectId': projectId,
        'description': description,
        'hwSets': {},  # No hardware checked out initially
        'users': []  # No users initially
    }
    
    # Insert the project into the collection
    result = projects.insert_one(project)
    
    return result.inserted_id is not None  # Return True if inserted, False otherwise

# Function to add a user to a project
def addUser(client, projectId, userId):
    db = client['User_DB']
    projects = db['projects']
    
    project = projects.find_one({'projectId': projectId})
    if not project:
        return False  # Project not found
    
    result = projects.update_one(
        {'projectId': projectId},
        {'$addToSet': {'users': userId}}
    )
    
    return result.modified_count > 0

# Function to update hardware usage in a project
def updateUsage(client, projectId, hwSetName, qty):
    db = client['User_DB']
    projects = db['projects']
    
    project = projects.find_one({'projectId': projectId})
    if not project:
        return False  # Project not found
    
    hwSets = project.get('hwSets', {})
    current_qty = hwSets.get(hwSetName, 0)
    new_qty = current_qty + qty
    
    if new_qty < 0:
        return False  # Cannot have negative quantity
    
    hwSets[hwSetName] = new_qty
    result = projects.update_one(
        {'projectId': projectId},
        {'$set': {'hwSets': hwSets}}
    )
    
    return result.modified_count > 0

# Function to check out hardware for a project
def checkOutHW(client, projectId, hwSetName, qty, userId):
    # Check if the project exists and the user is part of the project
    db = client['User_DB']
    projects = db['projects']
    
    project = projects.find_one({'projectId': projectId})
    if not project:
        return False  # Project not found
    
    if userId not in project.get('projects', []):
        return False  # User not part of the project
    
    # Try to request space in hardware set
    success = HardwareDB.requestSpace(client, hwSetName, qty)
    if not success:
        return False  # Not enough hardware availability
    
    # Update the project's hardware usage
    updated = updateUsage(client, projectId, hwSetName, qty)
    if not updated:
        # If updating usage fails, roll back the hardware availability
        HardwareDB.updateAvailability(client, hwSetName, HardwareDB.queryHardwareSet(client, hwSetName)['availability'] + qty)
        return False
    
    return True

# Function to check in hardware for a project
def checkInHW(client, projectId, hwSetName, qty, userId):
    # First, check if the project exists and the user is part of the project
    db = client['User_DB']
    projects = db['projects']
    
    project = projects.find_one({'projectId': projectId})
    if not project:
        return False  # Project not found
    
    if userId not in project.get('peojects', []):
        return False  # User not part of the project
    
    hwSets = project.get('hwSets', {})
    current_qty = hwSets.get(hwSetName, 0)
    if current_qty < qty:
        return False  # Cannot check in more than checked out
    
    # Update hardware availability
    success = HardwareDB.returnSpace(client, hwSetName, qty)
    if not success:
        return False  # Could not update hardware availability
    
    # Update the project's hardware usage
    updated = updateUsage(client, projectId, hwSetName, -qty)
    if not updated:
        # If updating usage fails, roll back the hardware availability
        HardwareDB.updateAvailability(client, hwSetName, HardwareDB.queryHardwareSet(client, hwSetName)['availability'] - qty)
        return False
    
    return True
