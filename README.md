# Construction Management API

A REST API for managing construction and structural engineering projects.

The application was created as a backend project combining database design, REST API development, authentication, automated testing, and containerization.

## Features

- Project management
- Structural element management
- Structural calculation management
- Material usage tracking
- Project dashboard and progress information
- Project bottleneck analysis
- User management
- User-to-project assignment
- JWT-based authentication
- Role-based authorization
- Password hashing
- SQL Server stored procedures
- SQL Server views
- Automated API and database integration tests

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Uvicorn

### Database

- Microsoft SQL Server
- T-SQL
- Stored Procedures
- SQL Views
- pyodbc

### Authentication

- JWT
- python-jose
- Passlib / bcrypt

### Testing

- pytest
- API and database integration tests

### DevOps / Tools

- Docker
- Docker Compose
- Git
- GitHub

## Project Architecture

```text
construction-management-api/
│
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── calculations.py
│   │   ├── elements.py
│   │   ├── materials.py
│   │   ├── projects.py
│   │   └── users.py
│   │
│   ├── schemas/
│   │   ├── calculation.py
│   │   ├── common.py
│   │   ├── element.py
│   │   ├── exceptions.py
│   │   ├── material.py
│   │   ├── project.py
│   │   └── user.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   └── security.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_calculations.py
│   ├── test_elements.py
│   ├── test_materials.py
│   ├── test_projects.py
│   └── test_users.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

## Database

The application uses Microsoft SQL Server as the primary database.

The database contains entities for:

- Projects
- Users
- Structural elements
- Calculations
- Materials
- Material usage
- Units
- Notes
- Project-user assignments

The project also uses database-level business logic through stored procedures and views.

Examples include:

- Safe project closing
- User assignment to projects
- Structural element creation
- Calculation creation
- Project status updates
- Project dashboard aggregation
- Project bottleneck detection
- Project health and progress analysis

## Authentication & Authorization

The API uses JWT-based authentication.

Passwords are stored as hashes rather than plaintext values.

The application defines three user roles:

- `ADMIN`
- `DESIGNER`
- `ASSISTANT`

Selected endpoints require authentication and/or specific user roles.

## API

The API is built with FastAPI and provides interactive OpenAPI documentation.

After starting the application, Swagger UI is available at:

```text
http://localhost:8000/docs
```

The main API areas include:

| Area | Description |
|---|---|
| `/auth` | Authentication |
| `/projects` | Project management |
| `/elements` | Structural elements |
| `/calculations` | Structural calculations |
| `/materials` | Material usage |
| `/users` | User management |

## Testing

The project uses pytest for automated testing.

The test suite covers:

- Authentication
- Authorization
- Projects
- Structural elements
- Materials
- Calculations
- Users
- Database interactions
- Validation and error handling

Current test status:

```text
86 passed
```

The tests use the actual SQL Server database and verify both API behavior and database-level operations.

## Docker

The API can be run using Docker Compose.

Build and start the application:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

To stop the application:

```bash
docker compose down
```

## Configuration

The application uses environment variables for configuration.

Create a `.env` file based on `.env.example`:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DB_SERVER=localhost
DB_NAME=project_management_db
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_DRIVER=ODBC Driver 17 for SQL Server
```

The `.env` file should not be committed to the repository.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/BartoszJaracz/construction-management-api.git
cd construction-management-api
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` based on `.env.example` and provide the local SQL Server connection details.

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

### 6. Open Swagger

```text
http://localhost:8000/docs
```

## Running Tests

Run the complete test suite with:

```bash
pytest
```

Expected result:

```text
86 passed
```

## Project Status

The application currently provides:

- REST API
- SQL Server integration
- JWT authentication
- Role-based authorization
- Stored procedures and views
- Automated tests
- Docker support
- Git/GitHub workflow

The project is being developed as a portfolio project demonstrating backend development, relational database design, API development, testing, and containerization.