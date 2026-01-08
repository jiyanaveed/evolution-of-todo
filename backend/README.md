# Evolution of Todo - Phase 2 Backend

This is the backend for Phase 2 of the Evolution of Todo application, built with FastAPI, SQLModel, and Neon Postgres.

## Features

- Full CRUD operations for tasks
- RESTful API endpoints
- Connection to Neon Postgres database
- Proper error handling and response codes
- CORS configured for localhost:3000
- Comprehensive testing suite
- Type hints and validation

## API Endpoints

- `GET /tasks` - Get all tasks (returns array of Task objects)
- `POST /tasks` - Create a new task (returns created Task, status 201)
- `GET /tasks/{id}` - Get a specific task (returns Task or 404)
- `PUT /tasks/{id}` - Update a task (returns updated Task or 404)
- `DELETE /tasks/{id}` - Delete a task (status 204 or 404)
- `PATCH /tasks/{id}/complete` - Toggle task completion status (returns updated Task or 404)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your Neon Postgres connection string
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Testing

Run the tests using pytest:
```bash
pytest
```

The test suite includes:
- Unit tests for CRUD operations
- Integration tests for API endpoints
- Error handling verification
- Status code validation

## Environment Variables

- `DATABASE_URL`: Your Neon Postgres connection string
- `PORT`: Port to run the application on (default: 8000)
- `LOG_LEVEL`: Logging level (default: info)

## Dependencies

- FastAPI
- SQLModel
- uvicorn
- psycopg2-binary
- python-dotenv
- pytest
- httpx