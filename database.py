# import pymysql
import pymysql.cursors
from typing import List, Optional
from models import Task, TaskIn, TaskUpdate
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+pymysql://root:password@localhost/task_management"

Base = declarative_base()

class TaskModel(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(500), nullable=True)
    due_date = Column(DateTime)
    priority = Column(Enum('Low', 'Medium', 'High'), default='Low')
    status = Column(Enum('Pending', 'In Progress', 'Completed'), default='Pending')
    creation_timestamp = Column(DateTime, default=datetime.utcnow)
    owner = Column(String(255))

# database init
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

class TaskManager:
    def __init__(self):
        self.db = SessionLocal()

    def create_task(self, task: TaskIn, username: str) -> Task:
        db_task = TaskModel(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            priority=task.priority,
            status=task.status,
            owner=username
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return Task.from_orm(db_task)

    def get_tasks(self, username: str, status: Optional[str] = None, priority: Optional[str] = None,
                  due_date: Optional[datetime] = None) -> List[Task]:
        query = self.db.query(TaskModel).filter(TaskModel.owner == username)

        if status:
            query = query.filter(TaskModel.status == status)
        if priority:
            query = query.filter(TaskModel.priority == priority)
        if due_date:
            query = query.filter(TaskModel.due_date == due_date)

        db_tasks = query.all()
        return [Task.from_orm(task) for task in db_tasks]

    def get_task_by_id(self, task_id: int, username: str) -> Optional[Task]:
        db_task = self.db.query(TaskModel).filter(TaskModel.task_id == task_id, TaskModel.owner == username).first()
        if db_task:
            return Task.from_orm(db_task)
        return None
    def update_task(self, task_id: int, task_update: TaskUpdate, username: str) -> Optional[Task]:
        db_task = self.db.query(TaskModel).filter(TaskModel.task_id == task_id, TaskModel.owner == username).first()
        if db_task:
            if task_update.title:
                db_task.title = task_update.title
            if task_update.description:
                db_task.description = task_update.description
            if task_update.due_date:
                db_task.due_date = task_update.due_date
            if task_update.priority:
                db_task.priority = task_update.priority
            if task_update.status:
                # Ensure that the status is one of the valid enum values
                valid_statuses = ['Pending', 'In Progress', 'Completed']
                if task_update.status in valid_statuses:
                    db_task.status = task_update.status
                else:
                    raise ValueError(f"Invalid status value: {task_update.status}. Must be one of {valid_statuses}")
            self.db.commit()
            self.db.refresh(db_task)
            return Task.from_orm(db_task)
        return None

    def delete_task(self, task_id: int, username: str) -> Optional[Task]:
        db_task = self.db.query(TaskModel).filter(TaskModel.task_id == task_id, TaskModel.owner == username).first()
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
            return Task.from_orm(db_task)
        return None

    def mark_as_completed(self, task_id: int, username: str) -> Optional[Task]:
        db_task = self.db.query(TaskModel).filter(TaskModel.task_id == task_id, TaskModel.owner == username).first()
        if db_task:
            db_task.status = 'Completed'
            self.db.commit()
            self.db.refresh(db_task)
            return Task.from_orm(db_task)
        return None

    # def delete_task(self, task_id: int, username: str) -> Optional[Task]:
    #     db_task = self.db.query(TaskModel).filter(TaskModel.task_id == task_id, TaskModel.owner == username).first()
    #     if db_task:
    #         self.db.delete(db_task)
    #         self.db.commit()
    #         return Task.from_orm(db_task)
    #     return None

task_manager = TaskManager()

def get_task_manager():
    return task_manager
