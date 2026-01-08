from setuptools import setup, find_packages

setup(
    name="evolution-of-todo-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "pydantic",
        "python-dotenv",
        "bcrypt",
        "PyJWT",
        "psycopg2-binary",
        "sqlalchemy"
    ],
)