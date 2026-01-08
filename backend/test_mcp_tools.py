"""
Test suite for MCP tools following the locked spec
"""
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from .models import Task
from .mcp_tools import TaskMCPTools


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",  # Use in-memory SQLite database for testing
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_task(session: Session):
    """Test CREATE operation as per locked spec"""
    tools = TaskMCPTools()
    user_id = "test_user_123"
    title = "Test task"

    result = tools.create_task(session, user_id, title)

    assert result["title"] == title
    assert result["completed"] is False
    assert result["user_id"] == user_id
    assert result["id"] is not None


def test_read_task(session: Session):
    """Test READ operation as per locked spec"""
    tools = TaskMCPTools()
    user_id = "test_user_123"
    title = "Test task"

    # Create a task first
    created = tools.create_task(session, user_id, title)
    task_id = created["id"]

    # Read the task
    result = tools.read_task(session, task_id, user_id)

    assert result is not None
    assert result["id"] == task_id
    assert result["title"] == title
    assert result["completed"] is False
    assert result["user_id"] == user_id


def test_update_task_title(session: Session):
    """Test UPDATE title operation as per locked spec"""
    tools = TaskMCPTools()
    user_id = "test_user_123"
    original_title = "Original task"
    new_title = "Updated task"

    # Create a task first
    created = tools.create_task(session, user_id, original_title)
    task_id = created["id"]

    # Update the task title
    result = tools.update_task(session, task_id, user_id, new_title=new_title)

    assert result is not None
    assert result["id"] == task_id
    assert result["title"] == new_title
    assert result["completed"] is False
    assert result["user_id"] == user_id


def test_update_task_completion(session: Session):
    """Test UPDATE completion operation as per locked spec"""
    tools = TaskMCPTools()
    user_id = "test_user_123"
    title = "Test task"

    # Create a task first
    created = tools.create_task(session, user_id, title)
    task_id = created["id"]

    # Update the task completion to True
    result = tools.update_task(session, task_id, user_id, completed=True)

    assert result is not None
    assert result["id"] == task_id
    assert result["completed"] is True
    assert result["user_id"] == user_id


def test_completion_constraint(session: Session):
    """Test that completed tasks cannot revert to incomplete"""
    tools = TaskMCPTools()
    user_id = "test_user_123"
    title = "Test task"

    # Create a task first
    created = tools.create_task(session, user_id, title)
    task_id = created["id"]

    # Update the task completion to True
    updated_to_complete = tools.update_task(session, task_id, user_id, completed=True)
    assert updated_to_complete["completed"] is True

    # Attempt to revert to incomplete (should raise ValueError)
    with pytest.raises(ValueError, match="A completed task cannot revert to incomplete"):
        tools.update_task(session, task_id, user_id, completed=False)


def test_delete_task(session: Session):
    """Test DELETE operation as per locked spec"""
    tools = TaskMCPTools()
    user_id = "test_user_123"
    title = "Test task to delete"

    # Create a task first
    created = tools.create_task(session, user_id, title)
    task_id = created["id"]

    # Verify task exists
    retrieved = tools.read_task(session, task_id, user_id)
    assert retrieved is not None

    # Delete the task
    success = tools.delete_task(session, task_id, user_id)
    assert success is True

    # Verify task no longer exists
    deleted = tools.read_task(session, task_id, user_id)
    assert deleted is None


def test_title_validation(session: Session):
    """Test that titles must be non-empty and have non-whitespace characters"""
    tools = TaskMCPTools()
    user_id = "test_user_123"

    # Test empty title
    with pytest.raises(ValueError, match="Title must be non-empty"):
        tools.create_task(session, user_id, "")

    # Test whitespace-only title
    with pytest.raises(ValueError, match="Title must be non-empty"):
        tools.create_task(session, user_id, "   ")

    # Test update with empty title
    created = tools.create_task(session, user_id, "Valid title")
    with pytest.raises(ValueError, match="Title must be non-empty"):
        tools.update_task(session, created["id"], user_id, new_title="")


def test_ownership_validation(session: Session):
    """Test that users can only access their own tasks"""
    tools = TaskMCPTools()
    user1_id = "user_1_123"
    user2_id = "user_2_456"
    title = "Test task"

    # Create a task for user 1
    created = tools.create_task(session, user1_id, title)
    task_id = created["id"]

    # Verify user 1 can access the task
    result1 = tools.read_task(session, task_id, user1_id)
    assert result1 is not None

    # Verify user 2 cannot access the task
    result2 = tools.read_task(session, task_id, user2_id)
    assert result2 is None