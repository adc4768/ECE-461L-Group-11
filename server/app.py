# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Import custom modules for database interactions
import usersDatabase as usersDB
import projectsDatabase as projectsDB
import hardwareDatabase as hardwareDB

# In this code, I do not provide details about the failure.
# That is, I just return the result "fail"; I do not return any details about the failure.
# I need to add the failure information.
# For example in the login() method, I just return the fact "fail" like this
#    if success:
#      return jsonify({'message' : 'LOGIN SUCCESS'}), 201
#    else:
#      return jsonify({'message' : 'LOGIN FAIL'}), 400
# But, we need to provide the detail like "User ID does not exist" or "The passeord is wrong"

# Additionally, we need to use different status codes such as 201 or 403 instead of 200 and 400.
# Each status code has a specific meaning, so we need to select the appropriate one accordingly.


# Define the MongoDB connection string
MONGODB_SERVER = "mongodb://localhost:27017/" 
# I now using this but to use this app by many people, I have to use remotehot
#So, this is tentative mongo server

# Initialize a new Flask web application
app = Flask(__name__)

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract data from request
    data = request.get_jason()
    userName = data.get('userName')
    userId = data.get('userId')
    password = data.get('password')

    # Connect to MongoDB    
    client = MongoClient(MONGODB_SERVER)

    # Attempt to log in the user using the usersDB module
    success = usersDB.login(client, userName, userId, password)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if success:
        return jsonify({'message' : 'LOGIN SUCCESS'}), 200
    else:
        return jsonify({'message' : 'LOGIN FAIL'}), 400


# Route for the main page (Work in progress)
#I cannot find out what to write in here
@app.route('/main')
def mainPage():
    # Extract data from request

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Fetch user projects using the usersDB module

    # Close the MongoDB connection
    client.close()
    # Return a JSON response
    return jsonify({})

# Route for joining a project
@app.route('/join_project', methods=['POST'])
def join_project():
    # Extract data from request
    data = request.get_json()
    projectName = data.get('projectName')
    projectId = data.get('projectId')
    description = data.get('description')

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Attempt to join the project using the usersDB module
    success = usersDB.joinProhect(client, projectName, projectId, description)
    # Close the MongoDB connection
    client.close()
    # Return a JSON response
    if success:
        return jsonify({'message':'JOIN PROJECT  SUCCESS'}),200
    else:
        return jsonify({'message':'JOIN PROJECT  FAIL'}),400
    
# Route for adding a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    # Extract data from request
    data = request.get_json()
    userName = data.get('userName')
    userId = data.get('userId')
    password = data.get('password')
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Attempt to add the user using the usersDB module
    success = usersDB.addUser(client, userName, userId, password)
    # Close the MongoDB connection
    client.close()
    # Return a JSON response
    if success :
        return jsonify({'message':'ADD USER SUCCESS'}),200
    else:
        return  jsonify({'message':'ADD USER FAIL'}),400

# Route for getting the list of user projects
@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    # Extract data from request
    userId = request.args.get('userId')
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Fetch the user's projects using the usersDB module
    projects = usersDB.getUserProjectsList(client, userId)
    # Close the MongoDB connection
    client.close()
    # Return a JSON response
    if projects is None:
        return jsonify({'message': 'FAIL'}), 400
    else:
        return jsonify({'projects': projects}), 200

# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    # Extract data from request
    data = request.get_json()
    projectName = data.get('projectName')
    projectId = data.get('projectId')
    description = data.get(description)
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Attempt to create the project using the projectsDB module
    success = projectsDB.createProject(client, projectName, projectId, description)
    # Close the MongoDB connection
    client.close()
    # Return a JSON response
    if success:
        return jsonify({'message': 'SUCCESS'}), 200
    return jsonify({'message': 'FAIL'}), 200

# Route for getting project information
# I am not sure what we are suposed to do. I think "methods = ['GET]",
# But the provided code is "methods = ['GET]". I gonna ask TA abut this
@app.route('/get_project_info', methods=['POST'])
def get_project_info():
    # Extract data from request

    # Connect to MongoDB

    # Fetch project information using the projectsDB module
    projectInfo = projectsDB.queryProject(client, projectId) 
    # I think we will use the queryProject() method, but I am not certain

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for getting all hardware names
@app.route('/get_all_hw_names', methods=['POST'])
def get_all_hw_names():
    # Connect to MongoDB

    # Fetch all hardware names using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for getting hardware information
@app.route('/get_hw_info', methods=['POST'])
def get_hw_info():
    # Extract data from request

    # Connect to MongoDB

    # Fetch hardware set information using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request
    data = request.get_json()
    client = data.get('client')
    projectId = data.get('projectId')
    hwSetName = data.get('hwSetName')
    qty = data.get('qty')
    userId = data.get('userId')
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Attempt to check out the hardware using the projectsDB module
    success = projectsDB.checkOutHW(client, projectId, hwSetName, qty, userId)
    # Close the MongoDB connection
    client.close()
    # Return a JSON response
    if success : 
        return jsonify({'message' : 'CHECK OUT SUCCESS'}),200
    else : 
        return jsonify({'message' : 'CHECK OUT FAIL'}),300

# Route for checking in hardware
@app.route('/check_in', methods=['POST'])
def check_in():
    # Extract data from request
    data = request.get_json()
    client = data.get('client')
    projectId = data.get('projectId')
    hwSetName = data.get('hwSetName')
    qty = data.get('qty')
    userId = data.get('userId')
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Attempt to check out the hardware using the projectsDB module
    success = projectsDB.checkInHW(client, projectId, hwSetName, qty, userId)
    # Close the MongoDB connection
    client.close()
    # Return a JSON response
    if success : 
        return jsonify({'message' : 'CHECK IN SUCCESS'}),200
    else : 
        return jsonify({'message' : 'CHECK IN FAIL'}),300

# Route for creating a new hardware set
@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to create the hardware set using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking the inventory of projects
@app.route('/api/inventory', methods=['GET'])
def check_inventory():
    # Connect to MongoDB

    # Fetch all projects from the HardwareCheckout.Projects collection

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Main entry point for the application
if __name__ == '__main__':
    app.run()

