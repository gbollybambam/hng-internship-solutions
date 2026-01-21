Country Currency & Exchange API

This is a Django REST Framework API that fetches country data from external sources, processes it to include currency exchange rates and estimated GDP, and caches the results in a MySQL database.

The API provides endpoints to retrieve all countries, filter them, and get status updates. It also generates a summary image of the cached data.

API Endpoints

All endpoints are prefixed with /api/.

Method

Endpoint

Description

POST

/countries/refresh

Triggers a refresh of all country and exchange rate data from external APIs. This populates and updates the database.

GET

/countries

Returns a list of all countries. Supports filtering and sorting.

GET

/countries?region=<name>

Returns all countries in the specified region (e.g., ?region=Africa).

GET

/countries?currency=<name>

Returns all countries using the specified currency (e.g., ?currency=NGN).

GET

/countries?sort=gdp_desc

Returns all countries sorted by estimated GDP in descending order.

GET

/countries/<name>

Returns the details for a single country by name (case-insensitive).

DELETE

/countries/<name>/delete

Deletes a country record from the database by name.

GET

/status

Shows the total number of cached countries and the timestamp of the last successful refresh.

GET

/countries/image

Serves a generated PNG image summarizing the API status (total countries, top 5 by GDP).

Local Setup & Installation

Follow these steps to run the project on your local machine.

1. Prerequisites

Python 3.10+

MySQL Server

Git

2. Clone the Repository

git clone <your-github-repo-url>
cd country-api


3. Set Up the Environment

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install required dependencies
pip install -r requirements.txt


4. Configure Environment Variables

Create a file named .env in the root of the project directory. Copy the contents of .env.example into it and fill in your database details.

.env.example:

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=3306


5. Set Up the Database

Log in to your MySQL server and create the database:

CREATE DATABASE your_db_name;


Run the Django migrations to create the tables:

python manage.py migrate


6. Run the Application

Start the development server:

python manage.py runserver


The API will be available at http://127.0.0.1:8000/api/.

7. Populate Data

Before you can use the GET endpoints, you must populate the database. Send a POST request to the refresh endpoint using an API client like Postman or REST Client:

POST http://127.0.0.1:8000/api/countries/refresh