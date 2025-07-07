# The FakeDB class provides methods for managing tasks in a fake database.
from models import Task


class FakeDB:
    def __init__(self):
        self.tasks = []

        """
        This function adds a task to a list of tasks and assigns it an ID based on the current number of
        tasks in the list.
        
        :param task: The `add_task` method takes a `Task` object as a parameter. This `Task` object is used
        to add a new task to the list of tasks stored in the object that the method is being called on. The
        method assigns an ID to the task based on the current number of tasks
        :type task: Task
        :return: The `add_task` method is returning the `task` object that was added to the `self.tasks`
        list after assigning it an id based on the current number of tasks in the list.
        """
    def add_task(self, task: Task):
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        return task

    def get_task(self, task_id: int):
        task = next((task for task in self.tasks if task.id == task_id), None)
        return task

    def get_tasks(self):
        return self.tasks

    def update_task(self, task_id: int, task_update):
        for task in self.tasks:
            if task.id == task_id:
                if task_update.title is not None:
                    task.title = task_update.title
                if task_update.description is not None:
                    task.description = task_update.description
                if task_update.completed is not None:
                    task.completed = task_update.completed
                return task
        return None

    def delete_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]


db = FakeDB()
