
"""
1. Libraries used:
   - FastAPI: For building the API.
   - pymysql: For MySQL database interaction.
   - uvicorn: For serving the FastAPI app.

2. i create user admin for authentication:
   - Created a basic authentication system with predefined users (admin, user).

3 Crud  methods
    Create, Read (all, by ID), Update, Delete tasks.


"""


from fastapi import FastAPI, HTTPException, Depends, Header, Query
from typing import List, Optional
from datetime import datetime
from models import Task, TaskIn, TaskUpdate
from database import get_task_manager

app = FastAPI()

# here is the authentication admin and user

USERS = {
    "admin": "admin",
    "user": "user"
}

def get_current_user(username: str = Header(...)) -> str:
    if username not in USERS:
        raise HTTPException(status_code=401, detail="Invalid username")
    return username
def check_if_admin(username: str = Depends(get_current_user)):
    if USERS.get(username) != "admin":
        raise HTTPException(status_code=403, detail="Only admins can perform this action")

def validate_priority(priority: Optional[str]) -> Optional[str]:
    valid_priorities = ["Low", "Medium", "High"]
    if priority and priority not in valid_priorities:
        raise HTTPException(status_code=400, detail="Invalid priority. Valid values are: Low, Medium, High.")
    return priority

def validate_status(status: Optional[str]) -> Optional[str]:
    valid_statuses = ["Pending", "Completed", "In Progress"]
    if status and status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status. Valid values are: Pending, Completed, In Progress.")
    return status






# for inputting the data 
@app.post("/tasks/", response_model=Task)
async def create_task(
    task: TaskIn, 
    task_manager=Depends(get_task_manager), 
    username: str = Depends(get_current_user)
):
    task.priority = validate_priority(task.priority)
    task.status = validate_status(task.status)

    return task_manager.create_task(task, username)
#get data

@app.get("/tasks/", response_model=List[Task])
async def get_all_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[datetime] = None,
    task_manager=Depends(get_task_manager),
    username: str = Depends(get_current_user)
):
    status = validate_status(status)
    priority = validate_priority(priority)
    
    return task_manager.get_tasks(username, status, priority, due_date)
#get data
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(
    task_id: int, 
    task_manager=Depends(get_task_manager), 
    username: str = Depends(get_current_user)
):
    task = task_manager.get_task_by_id(task_id, username)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not owned by you")
    return task
#for updating the data
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: int, 
    task: TaskUpdate, 
    task_manager=Depends(get_task_manager), 
    username: str = Depends(get_current_user)
):
    check_if_admin(username)

    updated_task = task_manager.update_task(task_id, task, username)
    if not updated_task:
        raise HTTPException(status_code=403, detail="Unauthorized to update this task")
    return updated_task

#patch for completed the data
@app.patch("/tasks/{task_id}/complete", response_model=Task)
async def mark_task_as_completed(
    task_id: int,
    task_manager=Depends(get_task_manager),
    username: str = Depends(get_current_user)
):
    check_if_admin(username)

    task = task_manager.get_task_by_id(task_id, username)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not owned by you")
    
    if task.status == "Completed":
        raise HTTPException(status_code=400, detail="Task is already completed")

    # Mark the task as completed
    completed_task = task_manager.mark_as_completed(task_id, username)
    if not completed_task:
        raise HTTPException(status_code=403, detail="Unauthorized to complete this task")
    return completed_task



#deleted data method
@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(
    task_id: int, 
    task_manager=Depends(get_task_manager), 
    username: str = Depends(get_current_user)
):
    # Ensure only admin can delete tasks
    check_if_admin(username)

    task = task_manager.delete_task(task_id, username)
    if not task:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this task")
    return task
