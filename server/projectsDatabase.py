# projectsDatabase.py

# Import necessary libraries and modules
from pymongo import MongoClient

'''
Structure of Project entry:
Project = {
    'projectName': projectName,
    'projectId': projectId,
    'description': description
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
        'description': description
    }
    
    # Insert the project into the collection
    result = projects.insert_one(project)
    
    return result.inserted_id is not None  # Return True if inserted, False otherwise
