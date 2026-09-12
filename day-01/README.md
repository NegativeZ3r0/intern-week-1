<!--• Project Overview • Problem Statement • Features • Technology Stack • Architecture • Database Design, where applicable • API Documentation, where applicable • Installation • Environment Variables • How to Run • Screenshots, where applicable • Challenges Faced • Solutions • Future Improvements -->

# Practical Assignment
Build an Employee Management CLI application with Add, Update, Delete, Search, List, Highest Salary, Average Salary and Department Filter features.

## Features
- Add an employee by providing its ID, name, Department and Salary
- Update the information of already added employee by providing it's ID
- Delete employee record by providing employee ID
- Search through employee recodes by providing it's ID or name
- List all employees and their information
- Filter employees by their department
- Find highest paid employee
- Find average salary of all employees

## Architecture
- defined `Employee` class to store information of an employe
- defined `EmployeeManager` class, which provides the methods to interface with the `Employee` class
- records are stored as a python dictionary, where key is unique employee ID and value is the corresponding `Employee` object

## Installation
- have python v3.13 or greater installed
- acquire `employee-management/main.py` file and place it in the working directory

## Usage
after following installation steps, run following command from the working directory
```bash
python main.py
```

## Challenges Faced
- Accounting for all possible edge cases and user inputs which can cause errors or unintentional results

## Solutions
- Multiple iterations of manual testing, bug fixing and error handling for specific input values
