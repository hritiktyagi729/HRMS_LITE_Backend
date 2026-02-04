functional requirement
    1. employee management
        The application should allow admin to :
            Add a new employee with the following details:
                Employee ID (unique)
                Full name
                Email Adress
                Department
            View a list of all employees
            Delete an employee
    2. Attendance Management
        The application should allow the admin to :
            Mark attendance for an employee with :
                Date
                Status (present/absent)
            view attendance records for each employee

Backend and database requirements
    Implement restful apis for all functionalities
    persist data using a database ( nosql or mysql)
    perform basic server-side validation
        required fields
        valid email formats
        duplicate employee handlings
    Handle invalid requests and error gracefully
        proper http status code
        meaningful error messages

                <!-- <input type="text" id = "employee_ulid" name="employee_ulid" placeholder="Enter Employee ULID to delete"> -->
                 <!-- <a class="btn btn-danger" href="{% url 'delete_employee' employee.ulid %}">Delete Employee</a> -->        