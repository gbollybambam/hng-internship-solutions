Dynamic Profile Endpoint: /me
This project implements a RESTful API endpoint in Python using the Django framework. The endpoint, /me, returns static user profile information combined with dynamic data, specifically a random cat fact fetched from a third-party API and a real-time UTC timestamp.

Prerequisites
You'll need the following installed on your system:

Python 3.8+

pip (Python package installer)

Setup Instructions
Follow these steps to get a local copy of the project running:

Clone the Repository:

git clone "repo-link"
cd profile_project # or the name of your cloned directory

Create and Activate Virtual Environment: It's strongly recommended to use a virtual environment to manage dependencies.

Create:
python -m venv venv

Activate (Linux/macOS):
source venv/bin/activate

Activate (Windows):
venv\Scripts\activate

Install Dependencies: Install all required libraries using the provided requirements.txt file.

pip install -r requirements.txt

Environment Variables
This project requires three environment variables to be set for the user profile data.

Action: Create a file named .env in the project's root directory and add the following variables:

Ini, TOML

# .env file
USER_EMAIL="your.email@example.com"
USER_NAME="Your Full Name"
USER_STACK="Python/Django"
DJANGO_SECRET_KEY='your secret key'
DEBUG= entervalue

Note: The .env file is included in .gitignore and should never be committed to the repository.

Run Locally
Ensure your virtual environment is activated.

Start the Django development server:

python manage.py runserver
The server should start running at http://127.0.0.1:8000/.

Endpoint Details
The required dynamic profile data can be accessed by sending a GET request to the following URL:

Method: GET

URL: http://127.0.0.1:8000/me/

Expected Response Format (200 OK)
JSON

{
  "status": "success",
  "user": {
    "email": "your.email@example.com",
    "name": "Your Full Name",
    "stack": "Python/Django"
  },
  "timestamp": "2025-10-15T19:30:00.123456Z", // Current UTC time in ISO 8601
  "fact": "A random cat fact fetched from https://catfact.ninja/fact"
}
