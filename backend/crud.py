from sqlmodel import Session, select
from typing import List, Optional
from .models import Task, User, Message, Conversation
import bcrypt


def get_tasks(session: Session) -> List[Task]:
    """
    Retrieve all tasks from the database.
    """
    tasks = session.exec(select(Task)).all()
    return tasks


def get_task(session: Session, task_id: int) -> Optional[Task]:
    """
    Retrieve a specific task by ID from the database.
    """
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    return task


def create_task(session: Session, title: str, description: Optional[str], user_id: str) -> Task:
    """
    Create a new task in the database.
    """
    task = Task(title=title, description=description, completed=False, user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task_id: int, user_id: str, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Task]:
    task = get_task_by_user(session, task_id, user_id)
    if task:
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            # Apply completion constraint: can only go false→true
            if task.completed == True and completed == False:
                # Cannot revert a completed task to incomplete
                pass  # Don't update the completion status
            else:
                task.completed = completed
        session.add(task)
        session.commit()
        session.refresh(task)
    return task


def delete_task(session: Session, task_id: int, user_id: str) -> bool:
    """
    Delete a task from the database by ID.
    """
    task = get_task_by_user(session, task_id, user_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False


def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Toggle the completion status of a task in the database.
    NOTE: This function is being kept for backwards compatibility with Phase II,
    but for Phase III compliance, use update_task with completed=True only.
    """
    task = get_task_by_user(session, task_id, user_id)
    if task:
        # Apply completion constraint: can only go false→true
        if task.completed == True:
            # Task is already completed, can't toggle back to incomplete
            return task
        else:
            # Task is incomplete, can toggle to completed
            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)
    return task


def get_tasks_by_user(session: Session, user_id: str) -> List[Task]:
    """
    Retrieve all tasks for a specific user from the database.
    """
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks


def get_task_by_user(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Retrieve a specific task by ID for a specific user from the database.
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by their email from the database.
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    """
    Retrieve a user by their ID from the database.
    """
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user


def create_user(session: Session, email: str, password: str) -> User:
    """
    Create a new user in the database with hashed password.
    """
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create new user instance
    user = User(email=email, password_hash=hashed_password)

    # Add to session and commit
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def create_conversation(session: Session, user_id: str) -> Conversation:
    """
    Create a new conversation in the database.
    """
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def get_conversation(session: Session, conversation_id: int, user_id: str) -> Optional[Conversation]:
    """
    Retrieve a specific conversation by ID for a specific user from the database.
    """
    statement = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)
    conversation = session.exec(statement).first()
    return conversation


def get_messages(session: Session, conversation_id: int, user_id: str) -> List[Message]:
    """
    Retrieve conversation history for a specific conversation and user.
    Ordered by creation date.
    """
    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id
    ).order_by(Message.created_at)
    return session.exec(statement).all()


def save_message(session: Session, conversation_id: int, user_id: str, role: str, content: str) -> Message:
    """
    Persist a message to the database.
    """
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message
