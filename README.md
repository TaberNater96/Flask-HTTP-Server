# Flask TODO API & Application

A simple TODO application built with Python, Flask, and PostgreSQL. This project serves as a learning exercise for backend engineering principles, including RESTful API design, database interaction with SQLAlchemy, and basic frontend integration. It's designed to be containerized with Docker for easy deployment.

## Table of Contents

- [Flask TODO API \& Application](#flask-todo-api--application)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [How It Works](#how-it-works)
  - [Project Structure](#project-structure)
  - [Features](#features)
  - [Technology Stack](#technology-stack)
  - [Setup and Installation](#setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [Local Development Setup](#local-development-setup)
  - [Running the Application](#running-the-application)
    - [Locally](#locally)
    - [With Docker](#with-docker)
  - [API Endpoints](#api-endpoints)
  - [Development Pipeline](#development-pipeline)
  - [Future Enhancements](#future-enhancements)

## Overview

This project implements a fully functional backend for a TODO list application. It provides RESTful API endpoints for Create, Read, Update, and Delete (CRUD) operations on TODO items. A minimalistic HTML/JavaScript frontend is included to interact with the API.

The primary focus is on a well-structured backend, demonstrating good practices for separation of concerns, database management, and API design.

## How It Works

The application follows a typical client-server architecture:

1.  **Frontend (Client):** A simple HTML page with JavaScript allows users to view, add, update, and delete TODO items.
2.  **User Interaction:** User actions on the frontend trigger JavaScript functions.
3.  **HTTP Requests:** JavaScript makes asynchronous HTTP requests (e.g., GET, POST, PUT, DELETE) to the backend Flask API.
4.  **Flask API (Backend):**
    *   Flask receives the incoming requests and routes them to the appropriate API endpoint handlers.
    *   Handlers process the request, validate data (if necessary), and interact with the service layer.
5.  **Service Layer (Optional):** Business logic is handled here before interacting with the database models.
6.  **Database Interaction (SQLAlchemy ORM):**
    *   The application uses SQLAlchemy to define database models (e.g., `Todo` item) and interact with the PostgreSQL database.
    *   Flask-SQLAlchemy simplifies this integration.
7.  **Database (PostgreSQL):** Stores all TODO items and their attributes.
8.  **HTTP Response:** The Flask API sends a JSON response back to the frontend, which then updates the UI accordingly.

## Project Structure

```
Flask HTTP Server/
├── .dockerignore               # Specifies files/directories to ignore for Docker build
├── .env                        # Environment variables (DB URL, secrets) - in .gitignore
├── .flaskenv                   # Flask specific environment variables (FLASK_APP, FLASK_ENV)
├── .gitignore                  # Specifies intentionally untracked files for Git
├── Dockerfile                  # Instructions to build the Docker image for the app
├── README.md                   # This file
├── config.py                   # Configuration settings (DevConfig, ProdConfig, etc.)
├── requirements.txt            # List of Python dependencies
├── run.py                      # Script to run the Flask development server
│
├── app/                        # Main application package
│   ├── __init__.py             # Initializes the Flask app, extensions, and Blueprints
│   ├── models.py               # SQLAlchemy database models
│   ├── schemas.py              # (Optional) Marshmallow schemas for serialization/validation
│   │
│   ├── api/                    # Blueprint for API routes
│   │   ├── __init__.py
│   │   └── routes.py           # Defines API endpoints
│   │
│   ├── assets/                 # Static files (CSS, JavaScript, images)
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   │
│   ├── templates/              # HTML templates (Jinja2)
│   │   ├── base.html
│   │   └── index.html
│   │
│   └── services/               # (Optional) Business logic layer
│       ├── __init__.py
│       └── todo_service.py
│
├── migrations/                 # Database migration scripts (Flask-Migrate/Alembic)
│   ├── versions/
│   └── ...
│
├── tests/                      # Unit and integration tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
│
└── venv/                       # Python virtual environment directory (IGNORED BY GIT)
    └── ...
```

## Features

*   RESTful API for managing TODO items.
*   Full CRUD (Create, Read, Update, Delete) operations.
*   PostgreSQL database integration using SQLAlchemy.
*   Database schema migrations managed by Flask-Migrate.
*   Simple web interface for interacting with the TODO list.
*   Docker support for containerization and deployment.

## Technology Stack

*   **Backend:** Python, Flask
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy (with Flask-SQLAlchemy)
*   **Migrations:** Flask-Migrate (uses Alembic)
*   **Frontend:** HTML, CSS, JavaScript (vanilla)
*   **Containerization:** Docker
*   **API Testing (Recommended):** Postman, Insomnia, or curl

## Setup and Installation

### Prerequisites

*   Python (3.8+ recommended)
*   Pip (Python package installer)
*   Git
*   PostgreSQL (running locally or accessible)
*   Docker (optional, for containerized deployment)

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd todo_app
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (Command Prompt):
    # venv\Scripts\activate.bat
    # On Windows (PowerShell):
    # venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    *   Create a `.env` file in the project root by copying `.env.example` (if provided) or creating it manually.
    *   Set your `DATABASE_URL` (e.g., `postgresql://user:password@host:port/database_name`) and `SECRET_KEY`.
    *   Example `.env` content:
        ```
        FLASK_APP=run.py
        FLASK_ENV=development
        DATABASE_URL="postgresql://youruser:yourpassword@localhost:5432/todo_db"
        SECRET_KEY="a_very_strong_and_random_secret_key"
        ```
    *   Create a `.flaskenv` file (or add to `.env`):
        ```
        FLASK_APP=run.py
        FLASK_ENV=development
        ```

5.  **Set up the database:**
    *   Ensure your PostgreSQL server is running and you have created the database specified in `DATABASE_URL`.
    *   Initialize the database migrations (if this is the first time):
        ```bash
        flask db init  # Only needed once per project
        flask db migrate -m "Initial migration"
        flask db upgrade
        ```
    *   For subsequent schema changes:
        ```bash
        flask db migrate -m "Description of changes"
        flask db upgrade
        ```

## Running the Application

### Locally

Ensure your virtual environment is activated and environment variables are set.
```bash
flask run
```
The application will typically be available at `http://127.0.0.1:5000/`.

### With Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t todo-app .
    ```

2.  **Run the Docker container:**
    Make sure to pass necessary environment variables (like `DATABASE_URL` if your database is external to Docker, or link to a Postgres container).
    ```bash
    docker run -p 5000:5000 --env-file .env todo-app
    # Or for a more complex setup with Docker Compose, you'd use a docker-compose.yml file.
    ```

## API Endpoints

All API endpoints are prefixed with `/api`.

*   **`POST /api/todos`**: Create a new TODO item.
    *   Request Body: `{ "title": "string", "description": "string (optional)" }`
*   **`GET /api/todos`**: Get all TODO items.
*   **`GET /api/todos/<id>`**: Get a specific TODO item by ID.
*   **`PUT /api/todos/<id>`**: Update an existing TODO item.
    *   Request Body: `{ "title": "string (optional)", "description": "string (optional)", "completed": "boolean (optional)" }`
*   **`DELETE /api/todos/<id>`**: Delete a TODO item.

## Development Pipeline

1.  **Local Development:**
    *   Create/checkout a feature branch.
    *   Code new features or fix bugs.
    *   Use the active virtual environment (`venv`) for dependency management.
    *   Install new packages with `pip install <package>` and update `requirements.txt` with `pip freeze > requirements.txt`.
    *   Run linters/formatters (e.g., Flake8, Black).
    *   Write and run unit/integration tests (from the `tests/` directory).
    *   Manually test API endpoints (e.g., with Postman) and frontend interactions.

2.  **Version Control (Git):**
    *   Commit changes regularly with clear messages.
    *   Push changes to the remote repository.
    *   Create Pull Requests (PRs) for review.

3.  **Continuous Integration (CI - Optional but Recommended):**
    *   Set up a CI pipeline (e.g., GitHub Actions, GitLab CI, Jenkins).
    *   The CI pipeline automatically:
        *   Checks out the code.
        *   Sets up the Python environment.
        *   Installs dependencies (`requirements.txt`).
        *   Runs linters and static analysis.
        *   Runs automated tests.
        *   (Optionally) Builds a Docker image.

4.  **Code Review & Merge:**
    *   Team members review PRs.
    *   Once approved and CI passes, merge the PR into the main branch (e.g., `main` or `develop`).

5.  **Staging/Deployment (Containerization with Docker):**
    *   The `Dockerfile` defines how to build a production-ready image of the application.
    *   Build the Docker image: `docker build -t todo-app .`
    *   Push the image to a container registry (e.g., Docker Hub, AWS ECR, Google GCR).
    *   Deploy the container to a staging or production environment. This might involve:
        *   Manually running `docker run ...`
        *   Using Docker Compose for multi-container setups (e.g., app + database).
        *   Using orchestration platforms like Kubernetes for more complex deployments.

6.  **Database Migrations in Production:**
    *   Before deploying a new version of the application with schema changes, run database migrations against the production database (e.g., `flask db upgrade` executed in a managed way).

## Future Enhancements

*   User authentication and authorization.
*   More robust error handling and input validation.
*   Comprehensive test suite (unit, integration, E2E).
*   Advanced frontend with a framework like React, Vue, or Angular.
*   CI/CD pipeline setup.
*   Deployment to a cloud platform.

---

Feel free to modify and expand upon this. Remember to replace `<repository-url>` with your actual Git repository URL once you create it.