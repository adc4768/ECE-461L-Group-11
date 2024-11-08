# hardwareSet.py

class hardwareSet:
    def __init__(self, hwName, capacity, availability=None, checkedOut=None):
        self.__hwName = hwName
        self.__capacity = capacity
        self.__availability = availability if availability is not None else capacity
        self.__checkedOut = checkedOut if checkedOut is not None else {}

    def initialize_capacity(self, qty):
        self.__capacity = qty
        self.__availability = qty

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
