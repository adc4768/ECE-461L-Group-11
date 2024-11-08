# hardwareDatabase.py

# Import necessary libraries and modules
from pymongo import MongoClient
from bson.objectid import ObjectId

'''
Structure of Hardware Set entry:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''

# Function to create a new hardware set
def createHardwareSet(client, hwSetName, initCapacity):
    db = client['User_DB'] 
    hardware_sets = db['hardwareSets']
    
    # Check if the hardware set already exists
    existing_set = hardware_sets.find_one({'hwName': hwSetName})
    if existing_set:
        return False  # Hardware set already exists
    
    # Create the hardware set document
    hardware_set = {
        'hwName': hwSetName,
        'capacity': initCapacity,
        'availability': initCapacity
    }
    
    result = hardware_sets.insert_one(hardware_set)
    
    return result.inserted_id is not None  # Return True if inserted, False otherwise

# Function to query a hardware set by its name
def queryHardwareSet(client, hwSetName):
    db = client['User_DB']
    hardware_sets = db['hardwareSets']
    
    hardware_set = hardware_sets.find_one({'hwName': hwSetName})
    
    return hardware_set

# Function to update the availability of a hardware set
def updateAvailability(client, hwSetName, newAvailability):
    db = client['User_DB']
    hardware_sets = db['hardwareSets']
    
    result = hardware_sets.update_one(
        {'hwName': hwSetName},
        {'$set': {'availability': newAvailability}}
    )
    
    return result.modified_count > 0  # Return True if a document was modified

# Function to request space from a hardware set
def requestSpace(client, hwSetName, amount):
    db = client['User_DB']
    hardware_sets = db['hardwareSets']
    
    # Check current availability
    hardware_set = hardware_sets.find_one({'hwName': hwSetName})
    if not hardware_set:
        return False  # Hardware set does not exist
    
    if hardware_set['availability'] < amount:
        return False  # Not enough availability
    
    # Update availability
    new_availability = hardware_set['availability'] - amount
    result = hardware_sets.update_one(
        {'hwName': hwSetName},
        {'$set': {'availability': new_availability}}
    )
    
    return result.modified_count > 0


# # Function to return hardware to the hardware set
# def returnSpace(client, hwSetName, amount):
#     db = client['User_DB']
#     hardware_sets = db['hardwareSets']
    
#     # Check current availability and capacity
#     hardware_set = hardware_sets.find_one({'hwName': hwSetName})
#     if not hardware_set:
#         return False  # Hardware set does not exist
    
#     capacity = hardware_set['capacity']
#     availability = hardware_set['availability']
    
#     if availability + amount > capacity:
#         return False  # Cannot exceed capacity
    
#     # Update availability
#     new_availability = availability + amount
#     result = hardware_sets.update_one(
#         {'hwName': hwSetName},
#         {'$set': {'availability': new_availability}}
#     )
    
#     return result.modified_count > 0

# Function to get all hardware set names
def getAllHwNames(client):
    db = client['User_DB']
    hardware_sets = db['hardwareSets']
    
    hw_names = hardware_sets.distinct('hwName')
    
    return hw_names
