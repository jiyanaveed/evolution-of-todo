from setuptools import setup, find_packages

setup(
    name="evolution-of-todo-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "sqlmodel==0.0.16",
        "uvicorn[standard]==0.24.0",
        "psycopg2-binary==2.9.9",
        "pydantic==2.5.0",
        "python-dotenv==1.0.0",
        "pytest==7.4.3",
        "httpx==0.25.2",
    ],
)