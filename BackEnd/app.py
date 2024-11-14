# Import necessary libraries and modules
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS  # Add this line
import logging
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
    print('userId: %s', userId)
    print('password: %s', password)
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
    data = request.get_json()
    app.logger.info('Received data: %s', data)
    
    userId = data.get('userId')
    projectId = data.get('projectId')

    # Log userId and projectId to the console
    app.logger.info('userId: %s', userId)
    app.logger.info('projectId: %s', projectId)

    if not userId or not projectId:
        app.logger.error('Missing userId or projectId')
        return jsonify({'message': 'Missing userId or projectId'}), 400  # Bad Request

    client = MongoClient(MONGODB_SERVER)
    try:
        success, message = usersDB.join_project(client, userId, projectId)
        app.logger.info('Join project result: %s, Message: %s', success, message)
    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        client.close()
        return jsonify({'message': 'An error occurred while updating the user project.'}), 500  # Internal Server Error
    
    client.close()
    if success:
        return jsonify({'message': message}), 200  # OK
    else:
        if message == 'Project does not exist.':
            return jsonify({'message': message}), 404  # Not Found
        elif message == 'Project already added to user joiningPJ.':
            return jsonify({'message': message}), 409  # Conflict
        elif message == 'User does not exist.':
            return jsonify({'message': message}), 404  # Not Found
        else:
            return jsonify({'message': message}), 400  # Bad Request





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
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)

    # Fetch all project information
    projects = client.your_database.projects.find({})
    project_list = []
    for project in projects:
        project_dict = {
            'projectId': project['projectId'],
            'projectName': project['projectName'],
            'description': project.get('description', '')
        }
        project_list.append(project_dict)

    # Close the MongoDB connection
    client.close()

    # Return a JSON response
    if project_list:
        return jsonify({'projects': project_list}), 200
    else:
        return jsonify({'message': 'No projects found.'}), 404


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
    

logging.basicConfig(level=logging.INFO)

@app.route('/get_user_projects', methods=['GET'])
def get_user_projects():
    logging.info('get_user_projects route triggered')
    userId = request.args.get('userId')
    print(f'userId: {userId}') # Print the value of userId to the console
    if not userId:
        return jsonify({'message': 'userId not provided.'}), 400

    client = MongoClient(MONGODB_SERVER)
    success, data = usersDB.get_evetyPRO_user_joining(client, userId)
    client.close()

    if success:
        return jsonify({'joiningPJ': data}), 200
    else:
        return jsonify({'message': data}), 400

# Main entry point for the application
if __name__ == '__main__':
    app.run(debug=True)