# Import necessary libraries and modules
from pymongo import MongoClient

'''
Structure of Project entry:
Project = {
    'projectName': projectName,
    'projectId': projectId,
    'description': description,
    'hwSets': {
        'HWset1': {'capacity': 100, 'availability': 100},
        'HWset2': {'capacity': 100, 'availability': 100}
    }
}
'''

# Function to query a project by its ID
def queryProject(client, projectId):
    db = client['User_DB']
    projects = db['projects']
    
    project = projects.find_one({'projectId': projectId})
    
    return project

# Function to create a new project
def createProject(client,userId, projectName, projectId, description):
    db = client['User_DB']
    projects = db['projects']
    users = db['users']
    
    # Check if the project already exists
    existing_project = projects.find_one({'projectId': projectId})
    if existing_project:
        return False  # Project already exists
    
    # Create the project document with hardware sets
    project = {
        'projectName': projectName,
        'projectId': projectId,
        'description': description,
        'hwSets': {
            'HWset1': {'capacity': 100, 'availability': 100},
            'HWset2': {'capacity': 100, 'availability': 100}
        }
    }
    
    # Insert the project into the collection
    result = projects.insert_one(project)
    if result.inserted_id:
        # Add the projectId to the user's joiningPJ array
        users.update_one(
            {'userId': userId},
            {'$addToSet': {'joiningPJ': projectId}}
        )
        return True, 'Project created and added to user joiningPJ.'
    else:
        return False, 'Failed to create project.'

# Function to check out hardware from a project
def checkOutHW(client, projectId, hwSetName, qty):
    db = client['User_DB']
    projects = db['projects']
    
    project = projects.find_one({'projectId': projectId})
    if not project:
        return False  # Project not found
    
    hwSets = project.get('hwSets', {})
    hwSet = hwSets.get(hwSetName)
    if not hwSet:
        return False, "No such HW exists"  # Hardware set not found in project
    
    availability = hwSet.get('availability', 0)
    if qty > availability:
        actual_qty = availability
        result_message = "SUCCESS! You checked out the maximum available items since your request exceeded the limit. "
    else :
        actual_qty = qty
        result_message = "SUCCESS!"

         # Not enough availability
    
    # Update availability
    hwSet['availability'] = availability - actual_qty
    hwSets[hwSetName] = hwSet
    
    # Update the project document
    result = projects.update_one(
        {'projectId': projectId},
        {'$set': {'hwSets': hwSets}}
    )
    
    return True, result_message  # Return True if updated

# Function to check in hardware to a project
def checkInHW(client, projectId, hwSetName, qty):
    db = client['User_DB']
    projects = db['projects']
    
    project = projects.find_one({'projectId': projectId})
    if not project:
        return False  # Project not found
    
    hwSets = project.get('hwSets', {})
    hwSet = hwSets.get(hwSetName)
    if not hwSet:
        return False  ,"Hardware set not found in project"# Hardware set not found in project
    
    capacity = hwSet.get('capacity', 0)
    availability = hwSet.get('availability', 0)
    used = capacity - availability

    if qty > used:
        actual_qty = used
        result_message = "SUCCESS! You checked in the maximum items since your request exceeded the limit. "
    else:
        actual_qty = qty
        result_message = "SUCCESS!"
    
    # Update availability
    hwSet['availability'] = availability + actual_qty
    hwSets[hwSetName] = hwSet
    
    # Update the project document
    result = projects.update_one(
        {'projectId': projectId},
        {'$set': {'hwSets': hwSets}}
    )
    
    return True, result_message  # Return True if updated
