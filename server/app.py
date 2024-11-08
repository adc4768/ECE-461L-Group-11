# app.py

# Import necessary libraries and modules
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Import custom modules for database interactions
import usersDatabase as usersDB
import projectsDatabase as projectsDB
import hardwareDatabase as hardwareDB

# Define the MongoDB connection string
MONGODB_SERVER = "mongodb+srv://Group11:LjIkXFETwAWP2YxP@cluster0.pg1fa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize a new Flask web application
app = Flask(__name__)

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract data from request
    data = request.get_json()
    userId = data.get('userId')
    password = data.get('password')

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to log in the user using the usersDB module
    success, response = usersDB.login(client, userId, password)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response with detailed messages and appropriate status codes
    if success:
        return jsonify({'message': response}), 200  
    else:
        return jsonify({'message': response}), 400

# Route for adding a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    # Extract data from request
    data = request.get_json()
    userId = data.get('userId')
    password = data.get('password')

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to add the user using the usersDB module
    success, message = usersDB.addUser(client, userId, password)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if success:
        return jsonify({'message': message}), 200  # Created
    else:
        return jsonify({'message': message}), 400  

# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    # Extract data from request
    data = request.get_json()
    projectName = data.get('projectName')
    projectId = data.get('projectId')
    description = data.get('description')

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to create the project using the projectsDB module
    success = projectsDB.createProject(client, projectName, projectId, description)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if success:
        return jsonify({'message': 'Project created successfully.'}), 200  # Created
    else:
        return jsonify({'message': 'Project creation failed. Project ID may already exist.'}), 400  

# Route for getting project information
@app.route('/get_project_info', methods=['GET'])
def get_project_info():
    # Extract 'projectId' from query parameters
    projectId = request.args.get('projectId')

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Fetch project information using the projectsDB module
    project = projectsDB.queryProject(client, projectId)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if project:
        # Remove ObjectId from the response
        project.pop('_id', None)
        return jsonify({'project': project}), 200  
    else:
        return jsonify({'message': 'Project not found.'}), 400

# Route for getting all hardware set names
@app.route('/get_all_hw_names', methods=['GET'])
def get_all_hw_names():
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Fetch all hardware set names using the hardwareDB module
    hw_names = hardwareDB.getAllHwNames(client)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    return jsonify({'hardwareSets': hw_names}), 200  

# Route for getting hardware information
@app.route('/get_hw_info', methods=['GET'])
def get_hw_info():
    # Extract 'hwSetName' from query parameters
    hwSetName = request.args.get('hwSetName')

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Fetch hardware set information using the hardwareDB module
    hardware_set = hardwareDB.queryHardwareSet(client, hwSetName)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if hardware_set:
        # Remove ObjectId from the response
        hardware_set.pop('_id', None)
        return jsonify({'hardwareSet': hardware_set}), 200  
    else:
        return jsonify({'message': 'Hardware set not found.'}), 400

# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request
    data = request.get_json()
    hwSetName = data.get('hwSetName')
    qty = int(data.get('qty', 0))
    projectID = data.get('projectId')

    if not projectID:
        return jsonify({'message': 'Project ID not provided.'}), 400

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to check out the hardware using the hardwareDB module
    success = hardwareDB.check_out(client, hwSetName, qty, projectID)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if success:
        return jsonify({'message': 'CHECK OUT SUCCESS'}), 200  
    else:
        return jsonify({'message': 'CHECK OUT FAIL'}), 400

# Route for checking in hardware
@app.route('/check_in', methods=['POST'])
def check_in():
    # Extract data from request
    data = request.get_json()
    hwSetName = data.get('hwSetName')
    qty = int(data.get('qty', 0))
    projectID = data.get('projectId')

    if not projectID:
        return jsonify({'message': 'Project ID not provided.'}), 400

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to check in the hardware using the hardwareDB module
    success = hardwareDB.check_in(client, hwSetName, qty, projectID)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if success:
        return jsonify({'message': 'CHECK IN SUCCESS'}), 200  
    else:
        return jsonify({'message': 'CHECK IN FAIL'}), 400

# Route for creating a new hardware set
@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    # Extract data from request
    data = request.get_json()
    hwSetName = data.get('hwSetName')
    initCapacity = int(data.get('initCapacity', 100))

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to create the hardware set using the hardwareDB module
    success = hardwareDB.createHardwareSet(client, hwSetName, initCapacity)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if success:
        return jsonify({'message': 'Hardware set created successfully.'}), 200
    else:
        return jsonify({'message': 'Hardware set creation failed. It may already exist.'}), 400  

# Main entry point for the application
if __name__ == '__main__':
    app.run(debug=True)
