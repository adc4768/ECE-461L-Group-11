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
    """
    Create a new hardware set in the database.
    
    :param client: MongoClient instance
    :param hwSetName: Name of the hardware set
    :param initCapacity: Initial capacity of the hardware set
    :return: True if created successfully, False otherwise
    """
    db = client['database_name']  # Replace 'database_name' with your actual database name
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
    
    # Insert the hardware set into the collection
    result = hardware_sets.insert_one(hardware_set)
    
    return result.inserted_id is not None  # Return True if inserted, False otherwise

# Function to query a hardware set by its name
def queryHardwareSet(client, hwSetName):
    """
    Query and return a hardware set from the database by its name.
    
    :param client: MongoClient instance
    :param hwSetName: Name of the hardware set to query
    :return: Hardware set document if found, None otherwise
    """
    db = client['database_name']
    hardware_sets = db['hardwareSets']
    
    hardware_set = hardware_sets.find_one({'hwName': hwSetName})
    
    return hardware_set

# Function to update the availability of a hardware set
def updateAvailability(client, hwSetName, newAvailability):
    """
    Update the availability of an existing hardware set.
    
    :param client: MongoClient instance
    :param hwSetName: Name of the hardware set to update
    :param newAvailability: New availability value
    :return: True if updated successfully, False otherwise
    """
    db = client['database_name']
    hardware_sets = db['hardwareSets']
    
    result = hardware_sets.update_one(
        {'hwName': hwSetName},
        {'$set': {'availability': newAvailability}}
    )
    
    return result.modified_count > 0  # Return True if a document was modified

# Function to request space from a hardware set
def requestSpace(client, hwSetName, amount):
    """
    Request a certain amount of hardware and update availability.
    
    :param client: MongoClient instance
    :param hwSetName: Name of the hardware set
    :param amount: Amount of hardware to request
    :return: True if request successful (availability decreased), False otherwise
    """
    db = client['database_name']
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

# Function to get all hardware set names
def getAllHwNames(client):
    """
    Get and return a list of all hardware set names.
    
    :param client: MongoClient instance
    :return: List of hardware set names
    """
    db = client['database_name']
    hardware_sets = db['hardwareSets']
    
    hw_names = hardware_sets.distinct('hwName')
    
    return hw_names
