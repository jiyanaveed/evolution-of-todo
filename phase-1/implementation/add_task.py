#!/usr/bin/env python3
"""
Implementation of the Add Task feature for Phase I of Evolution of Todo.
Following the specification and plan from the project documentation.
"""

import sys
from typing import Dict, List, Optional


class Task:
    """Represents a single task in the todo list."""

    def __init__(self, task_id: int, title: str, completed: bool = False):
        self.id = task_id
        self.title = title
        self.completed = completed


class TodoManager:
    """Manages the collection of tasks in memory."""

    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def generate_id(self) -> int:
        """Generate a unique ID for a new task."""
        new_id = self.next_id
        self.next_id += 1
        return new_id

    def add_task(self, title: str) -> Optional[Task]:
        """Add a new task with the given title."""
        if not self.is_valid_title(title):
            return None

        new_id = self.generate_id()
        task = Task(new_id, title, False)
        self.tasks.append(task)
        return task

    def is_valid_title(self, title: str) -> bool:
        """Validate that the title is not empty or just whitespace."""
        if not title:
            return False
        if not title.strip():
            return False
        if len(title) > 255:
            return False
        return True


def get_task_title_from_user() -> str:
    """Prompt the user for a task title."""
    title = input("Enter task title: ")
    return title


def display_confirmation(task: Task) -> None:
    """Display confirmation message after successful task addition."""
    print(f"Task '{task.title}' added successfully with ID: {task.id}")


def display_error_message(error_type: str) -> None:
    """Display appropriate error message based on error type."""
    if error_type == "empty_title":
        print("Task title cannot be empty. Please enter a valid title.")
    else:
        print("An error occurred while adding the task.")


def add_task_menu_option(todo_manager: TodoManager) -> bool:
    """
    Execute the Add Task menu option.
    Returns True if successful, False otherwise.
    """
    title = get_task_title_from_user()

    task = todo_manager.add_task(title)

    if task is not None:
        display_confirmation(task)
        return True
    else:
        display_error_message("empty_title")
        return False


def main():
    """Main function to demonstrate the Add Task feature."""
    print("Evolution of Todo - Add Task Feature")
    print("=====================================")

    # Initialize the todo manager
    todo_manager = TodoManager()

    # Demonstrate the add task functionality
    success = add_task_menu_option(todo_manager)

    if success:
        print(f"Current task count: {len(todo_manager.tasks)}")
    else:
        print("Task addition failed.")


if __name__ == "__main__":
    main()