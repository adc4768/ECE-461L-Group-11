class hardwareSet:
    def __init__(self):
        self.__capacity = 0
        self.__availability = 0
        self.__checkedOut = [0] * 1000  
        self.__hwName = "foo"

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
            self.__checkedOut[projectID] = self.__availability
            self.__availability = 0
            return -1  #If qty is larger than abailability, reuturn false
        self.__checkedOut[projectID] += qty
        self.__availability -= qty
        return 0  

    def check_in(self, qty, projectID):
        if qty > self.__checkedOut[projectID]:
            return -1  #If the qty is larger than the checkOut, retuen false
        self.__checkedOut[projectID] -= qty
        self.__availability += qty
        return 0 
