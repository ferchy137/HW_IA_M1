from fastapi import APIRouter, HTTPException, status
from models import Task, UpdateTaskModel, TaskList
from db import db
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tasks_router = APIRouter()


"""
Create a new task.

Endpoint to add a new task to the database.

Args:
    task (Task): The task to be created.

Returns:
    Task: The newly created task with assigned ID.
"""
@tasks_router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    try:
        # Input validation can be added here if needed
        created_task = db.add_task(task)
        logger.info(f"Task created successfully: {created_task}")
        return created_task
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the task")


"""
Retrieve a specific task by its ID.

Endpoint to fetch a single task from the database.

Args:
    task_id (int): The unique identifier of the task to retrieve.

Returns:
    Task: The task with the specified ID.

Raises:
    HTTPException: 404 error if the task is not found.
"""
@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    
    task = await db.get_task(task_id)  # Assuming db.get_task is an async function
    if task is None:
        logger.warning(f"Task with ID {task_id} not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    
    logger.info(f"Task retrieved successfully: {task}")
    return task


"""
Retrieve all tasks.

Endpoint to fetch all tasks from the database.

Returns:
    TaskList: A list of all tasks in the database.
"""
@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = await db.get_tasks()
    if tasks is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve tasks")
    return TaskList(tasks=tasks)


"""
Update an existing task.

Endpoint to modify a specific task in the database.

Args:
    task_id (int): The unique identifier of the task to update.
    task_update (UpdateTaskModel): The details to update for the task.

Returns:
    Task: The updated task.

Raises:
    HTTPException: 404 error if the task is not found.
"""
@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

"""
Deletes a task by its ID.

Args:
    task_id (int): The ID of the task to be deleted.

Returns:
    dict: A message indicating that the task was deleted successfully.
"""
@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}

#Endpoint to delete all tasks
"""
Delete all tasks.

Endpoint to remove all tasks from the database.

Returns:
    dict: A message confirming that all tasks have been deleted successfully.
"""
@tasks_router.delete("/")
async def delete_all_tasks():
    db.tasks = []
    return {"message": "All tasks deleted successfully"}
