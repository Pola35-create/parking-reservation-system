# API Description

## 1. Persons

### Get all persons

**Method:** `GET`  
**Endpoint:** `/persons`

Returns all persons stored in the system.

**Example request:**
```http
GET /persons
```

### Create a person

**Method:** `POST`  
**Endpoint:** `/persons`

Creates a new person.

**Example request body:**
```json
{
    "name": "John",
    "email": "john@example.com",
    "can_use_electric": true,
    "can_use_accessible": false,
    "can_use_dedicated": true
}
```

## 2. Parking spots

### Get all parking spots

**Method:** `GET`  
**Endpoint:** `/parking-spots`

Returns all parking spots stored in the system.

**Example request:**
```http
GET /parking-spots
```

### Get reservations for a parking spot

**Method:** `GET`
**Endpoint:** `/parking-spots/{id}/reservations`

Returns the reservations belonging to a specific parking spot.

**Example request:**
```http
GET /parking-spots/1/reservations
```

### Create a parking spot

**Method:** `POST`  
**Endpoint:** `/parking-spots`

Creates a new parking spot.

**Example request body:**
```json
{
  "spot_name": "E001",
  "type": "Standard"
}
```

## 3. Reservations

### Get all reservations

**Method:** `GET`  
**Endpoint:** `/reservations`

Returns all reservations stored in the system.

**Example request:**
```http
GET /reservations
```

### Create a reservation

**Method:** `POST`  
**Endpoint:** `/reservations`

Creates a new reservation.

**Example request body:**
```json
{
  "person_id": 1,
  "parking_spot_id": 1,
  "start_time": "2026-08-13T23:27:47.665Z",
  "end_time": "2026-08-13T23:27:47.665Z"
}
```

### Cancel a reservation

**Method:** `DELETE`  
**Endpoint:** `/reservations/{id}`

Cancels an existing reservation.

**Example request:**
```http
DELETE /reservations/1
```

## 4. Performing the API Operations
The API can be accessed through the FastAPI application. When the application is running, the available endpoints can also be tested using the automatically generated Swagger UI.

The Swagger documentation is available at:
```
/docs
```

Each endpoint can be executed directly from the Swagger interface by selecting the operation, providing the required parameters or request body, and selecting **Execute**.