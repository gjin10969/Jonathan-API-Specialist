Set up

Create a virtual environment and install FastAPI by running:

install dependency
pip install fastapi pymysql uvicorn


How to Run

First, set up the database:

Install MySQL if you haven't already.
Create a database by running the following SQL command:

CREATE DATABASE task_management;
Run the Python script using Uvicorn:

uvicorn app:app --reload
After running the script, open your browser and go to:

http://127.0.0.1:8000/docs
This will take you to the API documentation where you can view and interact with the REST API.

POST Method
It shows the authentication username, so use "admin" as the input. The correct format for the authentication username is either "admin" or "user."

In the parameters, the authentication username should be specified. For example:
{
  "title": "admin",
  "description": "admin",
  "due_date": "2025-01-27T11:44:59.044Z",
  "priority": "High",
  "status": "Pending"
}

GET Method
The GET method shows the data that you input in the POST request.

UPDATE Method
The UPDATE method allows you to modify the data you have previously entered.

PATCH Method
The PATCH method marks the data as completed.

DELETE Method
The DELETE method deletes the data.
