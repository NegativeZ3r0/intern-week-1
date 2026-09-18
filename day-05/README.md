<!--• Project Overview • Problem Statement • Features • Technology Stack • Architecture • Database Design, where applicable • API Documentation, where applicable • Installation • Environment Variables • How to Run • Screenshots, where applicable • Challenges Faced • Solutions • Future Improvements -->

# Project Overview
Build a JavaScript Employee Dashboard that consumes API/JSON data and supports listing, search, filter, sort, details, add, edit and delete operations.

## Architecture
- client-server approach
- data is stored as an array of objects on server side

## API
sigle route: `/api/employees` or `/api/employees/`
  - `GET`: gives the array of objects containing all employee data
  - `GET` with id param: gives object with the id in response
  - `POST`: is to add a new employee, details are provided in body of request
  - `PUT`: is to modify existing data of an object in employees array, id is mandatory param and details are provided in requests body
  - `DELETE` with id param: is to delete the object from employees array

## Installation
- have python and node installed
- acquire `employee-dashboard` folder and all of it's containts and place it in the working directory

## Usage
after following installation steps, run following command from the working directory
for running backend script on localhost:5069
```bash
node server/server.js
```
for serving frontend on localhost:4069
```bash
python -m http.server -d client/ -b 127.0.0.1 4069
```
access frontend on http://127.0.0.1:4069/ in browser

## Challenges faced
- dealing with CORS errors

## Solutions
- dynamically detecting origin of incoming requests and setting `Access-Control-Allow-Origin` and corresponding headers accordingly
