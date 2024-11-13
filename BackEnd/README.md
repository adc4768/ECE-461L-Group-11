
## How to Use

1. Move to the `BackEnd` directory:

   ```bash
   cd src
   ```

2. Run the following command to start the application:

   ```bash
   python3 app.py
   ```

   The program will now begin running, and you can access the API endpoints at `http://localhost:5000/`.

---

## Program Details

This program provides several key functions to manage user authentication, project creation, and hardware management. Here’s a brief overview of each function:

- **login()**: Checks if the provided `userId` and `password` match a registered user in the database. If they match, the function returns `True` and a success message; otherwise, it returns `False` with an error message.

- **add_user()**: Adds a new user to the database. You need to provide a unique `userId` and a `password`. If a user with the same `userId` already exists, the function will return an error, indicating that the user could not be added.

- **create_project()**: Creates a new project in the database. Each project includes fields such as `projectName`, `projectId`, and a `description`. Additionally, each project is automatically initialized with two hardware sets, `HWset1` and `HWset2`, each with a capacity of 100.

- **get_project_info()**: Retrieves the details of a specified project by `projectId`. This includes the `project’s name`, `description`, and the current status of hardware availability for `HWset1` and `HWset2`.*Perhaps, you do not need to this information*

- **check_out()**: Allows a user to check out a specified quantity of hardware from a project’s hardware set (`HWset1` or `HWset2`). The function decreases the availability of the hardware set if there is sufficient stock. If the requested quantity exceeds the available hardware, it returns an error message.The edge case where the user tries to check out more items than are available has already been implemented.

- **check_in()**: Allows a user to check in a specified quantity of hardware to a project’s hardware set (`HWset1` or `HWset2`). This function increases the availability of the hardware set, as long as it does not exceed the hardware’s capacity. The edge case where the user tries to check in more items than remaining one has already been implemented.

- **get_user_projects()**:  Retrieves the all projectId one user joining. 

---
