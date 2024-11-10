# Import necessary libraries and modules
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS  # Add this line

# Import custom modules for database interactions
import usersDatabase as usersDB
import projectsDatabase as projectsDB

# Define the MongoDB connection string
MONGODB_SERVER = "mongodb+srv://Group11:LjIkXFETwAWP2YxP@cluster0.pg1fa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize a new Flask web application
app = Flask(__name__)
CORS(app)  # Enable CORS

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
    
@app.route('/join', methods=['POST'])
def join():
    # Extract data from request
    data = request.get_json()
    userId = data.get('userId')
    projectId = data.get('projectId')

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to add the user using the usersDB module
    success, message = usersDB.join_project(client, userId, projectId)

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
    userId = data.get('userId')
    projectName = data.get('projectName')
    projectId = data.get('projectId')
    description = data.get('description')

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to create the project using the projectsDB module
    success = projectsDB.createProject(client, userId, projectName, projectId, description)

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

# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request
    data = request.get_json()
    projectId = data.get('projectId')
    hwSetName = data.get('hwSetName')
    qty = int(data.get('qty', 0))

    if not projectId:
        return jsonify({'message': 'Project ID not provided.'}), 400

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to check out the hardware using the projectsDB module
    success = projectsDB.checkOutHW(client, projectId, hwSetName, qty)

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
    projectId = data.get('projectId')
    hwSetName = data.get('hwSetName')
    qty = int(data.get('qty', 0))

    if not projectId:
        return jsonify({'message': 'Project ID not provided.'}), 400

    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Attempt to check in the hardware using the projectsDB module
    success = projectsDB.checkInHW(client, projectId, hwSetName, qty)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if success:
        return jsonify({'message': 'CHECK IN SUCCESS'}), 200  
    else:
        return jsonify({'message': 'CHECK IN FAIL'}), 400

# Main entry point for the application
if __name__ == '__main__':
    app.run(debug=True)