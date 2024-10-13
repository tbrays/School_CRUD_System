# Application User Guide

## Running the Application
1. **Start the Flask Application**:
   - Ensure your virtual environment is activated.
   - In your terminal or command prompt, navigate to the project directory.
   - Run the following command to start the Flask application:
     ```bash
     flask run
     ```
   - The application will be accessible at `http://127.0.0.1:5000/` in your web browser.

## Logging In
1. **Open the Login Page**:
   - Navigate to `http://127.0.0.1:5000/login` in your web browser.

2. **Enter Credentials**:
   - For an admin user, enter the following credentials (or use the credentials you set during setup):
     - Username: `admin`
     - Password: `admin123`

3. **Click the Login button** to access the admin dashboard.

## Adding a User
1. **Access User Management**:
   - From the admin dashboard, locate and click on the **Manage Users** option in the menu.

2. **Add New User**:
   - Fill in the required fields:
     - Username
     - Email
     - Role (e.g., Student, Teacher, Parent)
     - Password (ensure it meets security criteria)
   - Click on the **Add User** button.

## Editing a User
1. **View Existing Users**:
   - On the **Manage Users** page, you will see a list of registered users.

2. **Select User to Edit**:
   - Click the **Edit** button next to the user you wish to modify.

3. **Update User Information**:
   - Change the necessary fields (e.g., Email, Role).

4. **Save Changes**:
   - Click the **Save Changes** button to save the changes.

## Deleting a User
1. **View Existing Users**:
   - On the **Manage Users** page, find the user you want to delete.

2. **Delete User**:
   - Click the **Delete** button next to the user you wish to remove.

## Viewing a Timetable
1. **Access Timetable Management**:
   - From the admin dashboard, click on the **Manage Timetable** option in the menu.

2. **View Timetable**:
   - You will see a dropdown menu or a list of registered users. Select the user whose timetable you want to view (e.g., Student or Teacher).

## Adding a Timetable Entry
1. **Navigate to Manage Timetable**:
   - Ensure you are on the **Manage Timetable** page.

2. **Add New Timetable Entry**:
   - Fill in the required fields:
     - User (Student or Teacher)
     - Subject
     - Date and Time
   - Click the **Create Entry** button.

## Deleting a Timetable Entry
1. **View Timetable Entries**:
   - On the **Manage Timetable** page, locate the entry you wish to delete.

2. **Delete Entry**:
   - Click the **Delete** button next to the timetable entry you wish to remove.

## Toggling Security Settings
1. **Access Security Settings**:
   - From the admin dashboard, click on the **Settings** option in the menu.

2. **Toggle Security**:
   - Locate the **Security Settings** section.
   - Use the toggle switch to enable or disable security features, such as strong password enforcement or account lock after failed login attempts.

