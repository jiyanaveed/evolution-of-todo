import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from ..main import app
from ..database import get_session
from ..models import Task


# Create a test database engine
@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",  # Use in-memory SQLite database for testing
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(engine):
    def get_session_override():
        with Session(engine) as session:
            return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_task(client: TestClient):
    response = client.post("/tasks", json={"title": "Test task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert "id" in data


def test_read_tasks(client: TestClient):
    # Create a task first
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_read_task(client: TestClient):
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Single task"})
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Single task"
    assert data["completed"] is False
    assert data["id"] == task_id


def test_read_task_not_found(client: TestClient):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task(client: TestClient):
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Original task"})
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "Updated task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated task"
    assert data["id"] == task_id


def test_update_task_not_found(client: TestClient):
    response = client.put("/tasks/999", json={"title": "Updated task"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task(client: TestClient):
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Task to delete"})
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Verify the task is deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client: TestClient):
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_toggle_task_completion(client: TestClient):
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Toggle task"})
    task_id = create_response.json()["id"]

    # Toggle completion status
    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["completed"] is True

    # Toggle again to make sure it works both ways
    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["completed"] is False


def test_toggle_task_completion_not_found(client: TestClient):
    response = client.patch("/tasks/999/complete")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}