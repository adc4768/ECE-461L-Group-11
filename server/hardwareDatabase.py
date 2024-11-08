# hardwareDatabase.py

# Import necessary libraries and modules
from pymongo import MongoClient

'''
Structure of Hardware Set entry:
HardwareSet = {
    '_id': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity,
    'checkedOut': {}  # Dict mapping projectID to quantity
}
'''

# Function to create a new hardware set
def createHardwareSet(client, hwSetName, initCapacity):
    db = client['User_DB'] 
    hw_collection = db['HW']
    
    # Check if the hardware set already exists
    existing_set = hw_collection.find_one({'_id': hwSetName})
    if existing_set:
        return False  # Hardware set already exists

    # Create the hardware set document
    hardware_set = {
        '_id': hwSetName,
        'capacity': initCapacity,
        'availability': initCapacity,
        'checkedOut': {}  # Initialize empty dict
    }

    result = hw_collection.insert_one(hardware_set)

    return result.inserted_id is not None  # Return True if inserted, False otherwise

# Function to query a hardware set by its name
def queryHardwareSet(client, hwSetName):
    db = client['User_DB']
    hw_collection = db['HW']

    hardware_set = hw_collection.find_one({'_id': hwSetName})

    return hardware_set

# Function to update the availability and checkedOut of a hardware set
def updateHardwareSet(client, hwSetName, availability, checkedOut):
    db = client['User_DB']
    hw_collection = db['HW']

    result = hw_collection.update_one(
        {'_id': hwSetName},
        {'$set': {'availability': availability, 'checkedOut': checkedOut}}
    )

    return result.modified_count > 0  # Return True if a document was modified

# Function to check out hardware
def check_out(client, hwSetName, qty, projectID):
    db = client['User_DB']
    hw_collection = db['HW']

    # Fetch the hardware set
    hardware_set = hw_collection.find_one({'_id': hwSetName})
    if not hardware_set:
        return False  # Hardware set does not exist

    availability = hardware_set['availability']
    capacity = hardware_set['capacity']
    checkedOut = hardware_set.get('checkedOut', {})

    if qty > availability:
        return False  # Not enough availability

    # Update availability
    new_availability = availability - qty

    # Update checkedOut
    checkedOut[projectID] = checkedOut.get(projectID, 0) + qty

    # Update the hardware set in the database
    updated = updateHardwareSet(client, hwSetName, new_availability, checkedOut)

    return updated

# Function to check in hardware
def check_in(client, hwSetName, qty, projectID):
    db = client['User_DB']
    hw_collection = db['HW']

    # Fetch the hardware set
    hardware_set = hw_collection.find_one({'_id': hwSetName})
    if not hardware_set:
        return False  # Hardware set does not exist

    availability = hardware_set['availability']
    capacity = hardware_set['capacity']
    checkedOut = hardware_set.get('checkedOut', {})

    project_qty = checkedOut.get(projectID, 0)
    if qty > project_qty:
        return False  # Cannot check in more than the project has checked out

    # Update availability
    new_availability = availability + qty

    # Update checkedOut
    if qty == project_qty:
        del checkedOut[projectID]  # Remove the entry if zero
    else:
        checkedOut[projectID] = project_qty - qty

    # Update the hardware set in the database
    updated = updateHardwareSet(client, hwSetName, new_availability, checkedOut)

    return updated

# Function to get all hardware set names
def getAllHwNames(client):
    db = client['User_DB']
    hw_collection = db['HW']

    hw_names = hw_collection.distinct('_id')

    return hw_names

# hardwareSet class
class hardwareSet:
    def __init__(self, hwName, capacity, availability=None, checkedOut=None):
        self.__hwName = hwName
        self.__capacity = capacity
        self.__availability = availability if availability is not None else capacity
        self.__checkedOut = checkedOut if checkedOut is not None else {}

    def get_availability(self):
        return self.__availability

    def get_capacity(self):
        return self.__capacity

    def get_name(self):
        return self.__hwName

    def check_out(self, qty, projectID):
        if qty > self.__availability:
            return False  # Not enough availability
        self.__availability -= qty
        self.__checkedOut[projectID] = self.__checkedOut.get(projectID, 0) + qty
        return True  

    def check_in(self, qty, projectID):
        project_qty = self.__checkedOut.get(projectID, 0)
        if qty > project_qty:
            return False  # Cannot check in more than checked out
        self.__availability += qty
        if qty == project_qty:
            del self.__checkedOut[projectID]
        else:
            self.__checkedOut[projectID] = project_qty - qty
        return True 

    def to_dict(self):
        return {
            '_id': self.__hwName,
            'capacity': self.__capacity,
            'availability': self.__availability,
            'checkedOut': self.__checkedOut
        }
