# Amo Promo Technical Test

This project is a Django-based solution for two technical challenges:

1. **ETL Process for Airports Data**: Extracting, transforming, and loading data from an external API into a local database.
2. **Flight Combinator**: Providing travel combinations for round-trip flights with optimized pricing.

## Technologies Used

- **Django**: Framework for building the web application.
- **Requests**: Library for consuming external APIs.
- **PyJWT**: Library for creating and validating JWT tokens.

---

## Problem 1: ETL Process for Airports Data

### Description
The first problem addresses the need to bring external API data into our local database using an ETL process. The solution involves:

1. **Extracting**: Fetching data from an external API.
2. **Transforming**: Processing and validating the data.
3. **Loading**: Saving the data into the `Airports` table in the database.

### Implementation Details

- Two apps were created:
  - `airports`: Manages ETL functions and extracted data.
  - `logs`: Records logs for each ETL run.

- **ETL Workflow**:
  - At the start of an ETL run, a log entry is created with details like the target model, success state, and an initiation message.
  - A standardized API client class handles external requests.
  - Logs are updated throughout the process to capture errors or exceptions, indicating the point of failure if any.
  - Upon successful completion, the old data is cleared, and the new data is saved in the `Airports` table along with the associated log entry.

### Available Endpoints and Commands

1. **Load Airports Data**:
   - Endpoint: `POST /api/airports/load-airports/`
   - Django Command: `python manage.py import_airports`

2. **Retrieve Airports Data**:
   - `GET /api/airports/airport/`: Returns all airport data.
   - `GET /api/airports/airport/<int:pk>/`: Returns airport data filtered by primary key.

---

## Problem 2: Flight Combinator

### Description
The second problem involves consuming another external API to generate round-trip flight combinations between two locations. The external API does not fully meet the requirements, so the solution abstracts and manipulates the data to:

1. Provide a summary of the trip.
2. Calculate the total price.
3. Return all combinations of round-trip flights sorted by the lowest price.

### Implementation Details

- The solution validates inputs such as dates and IATA codes.
- Flights are filtered and combined based on departure and return dates.

### Available Endpoint

- `GET /api/airlines/airline-combinator/<str:from_iata>/<str:to_iata>/<str:departure_date>/<str:return_date>`

---

## Authentication

All endpoints are protected by JWT authentication. Users must authenticate and include a valid token in the request headers to access protected routes.

### Authentication Workflow

1. **Login**:
   - Endpoint: `POST /api/token`
   - Request Body:
     ```json
     {
       "username": "amopromo",
       "password": "1234"
     }
     ```
   - Response: JWT token.

2. **Access Protected Endpoints**:
   - Include the token in the `Authorization` header:
     ```
     Authorization: Bearer <your_token>
     ```

3. A custom decorator validates the token for each HTTP request, returning a 401 status code if validation fails.

---

## How to Run the Project

1. **Set Up the Environment**:
   - Clone the repository.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Set up the database and migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
   - Create superuser to authenticate, with the credentials username: 'amopromo' and password '1234' or any credential you prefer you will use this user to authenticate and receive the jwt token in the `/api/token/` routine
     ```bash
     python manage.py createsuperuser
     ```

2. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

3. **Execute ETL Process**:
   - Using the API: `POST /api/airports/load-airports/`
   - Using Django Command:
     ```bash
     python manage.py import_airports
     ```

4. **Test the Flight Combinator**:
   - Access the endpoint: `/api/airlines/airline-combinator/<from_iata>/<to_iata>/<departure_date>/<return_date>`

---

## API URL

The API is hosted at the following URL:

[https://amopromo-technical-test-old-sea-5514.fly.dev/](https://amopromo-technical-test-old-sea-5514.fly.dev/)

---
