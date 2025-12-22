#!/usr/bin/env python3
"""
Evolution of Todo - Phase I
Python console-based in-memory Todo application
Following Spec-Driven Development principles and project constitution
"""

import sys
from typing import Dict, List, Optional


class Task:
    """Represents a single task in the todo list."""

    def __init__(self, task_id: int, title: str, completed: bool = False):
        self.id = task_id
        self.title = title
        self.completed = completed

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        return f"{self.id}. {status} {self.title}"


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

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_title: str) -> bool:
        """Update the title of an existing task."""
        if not self.is_valid_title(new_title):
            return False

        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.title = new_title
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def toggle_task_completion(self, task_id: int) -> bool:
        """Toggle the completion status of a task."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = not task.completed
        return True

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.tasks


def display_menu():
    """Display the main menu options."""
    print("\nEvolution of Todo - Main Menu")
    print("=============================")
    print("1. Add Task")
    print("2. View Task List")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Exit")
    print()


def get_user_choice() -> str:
    """Get the user's menu choice."""
    return input("Select an option (1-6): ").strip()


def add_task_menu_option(todo_manager: TodoManager) -> None:
    """Execute the Add Task menu option."""
    title = input("Enter task title: ")

    task = todo_manager.add_task(title)

    if task is not None:
        print(f"Task '{task.title}' added successfully with ID: {task.id}")
    else:
        print("Task title cannot be empty. Please enter a valid title.")


def view_task_list_menu_option(todo_manager: TodoManager) -> None:
    """Execute the View Task List menu option."""
    tasks = todo_manager.get_all_tasks()

    if not tasks:
        print("No tasks in the list.")
        return

    print("\nTask List:")
    print("ID  | Status | Title")
    print("----|--------|------")
    for task in sorted(tasks, key=lambda t: t.id):
        status = "[x]" if task.completed else "[ ]"
        print(f"{task.id:<3} | {status}    | {task.title}")


def update_task_menu_option(todo_manager: TodoManager) -> None:
    """Execute the Update Task menu option."""
    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Invalid task ID. Please enter a number.")
        return

    task = todo_manager.get_task_by_id(task_id)
    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    new_title = input(f"Enter new title for task {task_id}: ")

    if todo_manager.update_task(task_id, new_title):
        print(f"Task {task_id} updated successfully: '{new_title}'")
    else:
        print("Task title cannot be empty. Please enter a valid title.")


def delete_task_menu_option(todo_manager: TodoManager) -> None:
    """Execute the Delete Task menu option."""
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid task ID. Please enter a number.")
        return

    if todo_manager.delete_task(task_id):
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Task with ID {task_id} not found.")


def mark_task_complete_menu_option(todo_manager: TodoManager) -> None:
    """Execute the Mark Task Complete menu option."""
    try:
        task_id = int(input("Enter task ID to mark as complete: "))
    except ValueError:
        print("Invalid task ID. Please enter a number.")
        return

    task = todo_manager.get_task_by_id(task_id)
    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    # Toggle the completion status
    was_completed = task.completed
    success = todo_manager.toggle_task_completion(task_id)

    if success:
        new_status = "pending" if was_completed else "completed"
        print(f"Task {task_id} marked as {new_status}: '{task.title}'")
    else:
        print(f"Failed to update task {task_id}.")


def main():
    """Main application loop."""
    print("Welcome to Evolution of Todo - Phase I")
    print("A Python console-based in-memory Todo application")

    todo_manager = TodoManager()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            add_task_menu_option(todo_manager)
        elif choice == "2":
            view_task_list_menu_option(todo_manager)
        elif choice == "3":
            update_task_menu_option(todo_manager)
        elif choice == "4":
            delete_task_menu_option(todo_manager)
        elif choice == "5":
            mark_task_complete_menu_option(todo_manager)
        elif choice == "6":
            print("Thank you for using Evolution of Todo. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please select a number between 1 and 6.")

        # Pause briefly to allow user to read output
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()