from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Database Model
class Task(BaseModel):
    task_id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    priority: str
    status: str
    creation_timestamp: datetime
    owner: str

    class Config:
        orm_mode = True  
        from_attributes = True 
# for task creation schema
class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    priority: str
    status: str

#  for task update
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None
