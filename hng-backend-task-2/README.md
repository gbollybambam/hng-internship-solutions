# 🧙‍♂️ Backend Wizard — String Analyzer Service (HNGi13 - Stage 1)

**Deployed API Base URL:** `https://web-production-f845e.up.railway.app/`
**Stack:** Python, Django, Django REST Framework (DRF), Gunicorn, WhiteNoise, PostgreSQL

---

## Project Overview

This is a RESTful API service that analyzes an input string and computes several properties (length, word count, palindrome status, character frequency, and SHA-256 hash). The service stores these properties and supports complex retrieval and filtering, including **Natural Language Queries**.

---

## 1. Local Setup and Installation

### Prerequisites
* Python 3.8+
* Git
* A virtual environment tool (`venv` is assumed).

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone YOUR_GITHUB_REPO_LINK
    cd hng-backend-task-2
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Use venv\Scripts\activate on Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create .env File:**
    Create a file named `.env` in the project root and add basic settings:
    ```env
    SECRET_KEY="A_SAFE_LOCAL_KEY_FOR_TESTING_ONLY"
    DJANGO_DEBUG=True
    ```

5.  **Run Migrations (Local SQLite):**
    ```bash
    python manage.py migrate
    ```

6.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```
    The API will be accessible at `http://127.0.0.1:8000/strings/`.

---

## 2. API Endpoints

All endpoints are relative to the **Base URL**. The API is tested and functional.

| No. | Description | Method | URL Path | Success |
| :--- | :--- | :--- | :--- | :--- |
| **1.** | **Create/Analyze String** | `POST` | `/strings/` | `201 Created` |
| **2.** | **Get Specific String** | `GET` | `/strings/{string_value}/` | `200 OK` |
| **3.** | **Get All Strings (Filtering)** | `GET` | `/strings/?is_palindrome=true&min_length=5...` | `200 OK` |
| **4.** | **Natural Language Filter** | `GET` | `/strings/filter-by-natural-language/?query=...` | `200 OK` |
| **5.** | **Delete String** | `DELETE` | `/strings/{string_value}/` | `204 No Content` |

---

## 3. Deployment Details (Railway)

* **Database:** PostgreSQL is used in production.
* **Startup Logic:** The `Procfile` executes the **`start.sh`** script, which ensures **`python manage.py migrate`** runs successfully before launching Gunicorn, resolving all previous deployment crashes.
* **Static Files:** **WhiteNoise** is configured to correctly serve all Django REST Framework assets for the browsable API interface.

---

**You are now fully ready to submit the task!** Go to Slack and use the `/stage-one-backend` command with your live URL and GitHub link.
