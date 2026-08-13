# User Manual

## 1. Starting the System

Make sure Docker is installed and running.

From the project directory, run:

```bash
docker compose up --build
```

The application and database are initialized automatically.

## 2. Accessing the API

Once the application is running, open the FastAPI Swagger interface:

```
http://localhost:8000/docs
```

The Swagger UI provides an interactive interface for all available API operations.

## 3. Using the API
To perform an operation:

### 1. Select an endpoint in Swagger.
### 2. Click Try it out.
### 3. Enter the required parameters or request body.
### 4. Click Execute.
### 5. Review the returned response.

The main operations allow users to:

- Manage persons.
- View parking spots.
- View reservations for parking spots.
- Create reservations.
- Retrieve reservations.
- Cancel reservations.

## 4. Stopping the System

To stop the application, press Ctrl + C or run:

```bash
docker compose down
```

No separate Python or database installation is required because the system runs inside Docker.