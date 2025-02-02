# CSV Upload API 

## Overview
This project provides a Django REST Framework (DRF) API for uploading and processing user data from a CSV file. The API validates and stores user information while handling errors gracefully.

## Features
- Upload a CSV file via a POST API endpoint.
- Validate CSV content (name, email, age constraints).
- Save valid records into a `User` model.
- Return a response with saved and rejected records, along with error details.
- Web UI to upload files and view saved records.
- Duplicate emails are skipped without causing errors.

## Technologies Used
- Django
- Django REST Framework
- Bootstrap (for UI styling)

## Installation & Setup

### Prerequisites
- Python 3.x
- pip
- virtualenv (recommended)

### Steps to Setup
1. **Clone the repository**
   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```
2. **Create a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations**
   ```sh
   python manage.py migrate
   ```
5. **Run the development server**
   ```sh
   python manage.py runserver
   ```
6. **Access the Web UI**
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## API Endpoints

### 1. Upload CSV File
**Endpoint:**
```
POST /upload/
```
**Request:**
- Upload a CSV file with `name`, `email`, and `age` columns.
- Must be in `.csv` format.

**Response Example:**
```json
{
    "total_saved": 3,
    "total_rejected": 1,
    "saved_records": [
        {"name": "Alice", "email": "alice@example.com", "age": "30"}
    ],
    "errors": [
        {"name": "", "email": "invalid@example", "age": "-5", "error": {"age": "Age must be between 0 and 120."}}
    ]
}
```

### 2. View Saved Records
**Endpoint:**
```
GET /saved-records/
```
**Response:**
- Returns all saved user records in a table view.

## Validation Rules
- **Name:** Must be a non-empty string.
- **Email:** Must be a valid email format and unique.
- **Age:** Must be an integer between `0-120`.

## UI Screens
### 1. CSV Upload Page
- Upload CSV files.
- View validation results and saved/rejected records.

### 2. Saved Records Page
- Displays stored user data in a table format.

## Running Tests
To run unit tests:
```sh
python manage.py test
```

## Sample Test Files
- ` New_Data.csv` - Example input CSV file.
- Expected HTML-based table display - A visual representation of how the saved records will appear in the HTML table on the web UI..

## Author
- **Sreejith S** - [GitHub](https://github.com/sreejith-0087)


