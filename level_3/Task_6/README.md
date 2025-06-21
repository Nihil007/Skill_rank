# Skill Rank - Task 6

This project is a full-stack authentication system with a FastAPI backend and a React (Vite) frontend. It supports user registration, login, password reset via email, protected dashboard, and comprehensive student management system.

---

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Backend Setup (FastAPI)](#backend-setup-fastapi)
- [Frontend Setup (React + Vite)](#frontend-setup-react--vite)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Development Workflow](#development-workflow)
- [Notes](#notes)

---

## Project Structure

```
Task_6/
  app/                # FastAPI backend
    ├── main.py       # Main application entry point
    ├── auth_routes.py # Authentication endpoints
    ├── students.py   # Student management endpoints
    ├── json_handler.py # JSON data operations
    ├── students_data.json # Student data storage
    └── requirements.txt
  auth-frontend/      # React frontend
    ├── src/
    │   ├── components/
    │   │   ├── Auth/     # Authentication components
    │   │   ├── Dashboard.jsx # Main dashboard
    │   │   └── StudentsDashboard.jsx # Student management interface
    │   └── api/
    │       ├── auth.js   # Authentication API calls
    │       └── students.js # Student management API calls
    └── package.json
```

---

## Features

### Authentication System
- User registration with email verification
- Secure login with JWT tokens
- Password reset via email
- Protected routes and dashboard access

### Student Management System
- **CRUD Operations**: Create, Read, Update, Delete students
- **Course Management**: Add students to multiple courses with grades
- **Filtering**: Filter students by course
- **Grade Management**: Update individual course grades
- **Data Persistence**: JSON-based data storage
- **Real-time Updates**: Immediate UI updates after operations

### User Interface
- Modern Material-UI design
- Responsive layout for all devices
- Interactive data tables
- Form validation and error handling
- Success/error notifications

---

## Backend Setup (FastAPI)

1. **Navigate to the backend directory:**
   ```sh
   cd app
   ```
2. **Create a virtual environment (recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up your `.env` file** (see [Environment Variables](#environment-variables))
5. **Run the FastAPI server:**
   ```sh
   uvicorn main:app --reload
   ```
   The backend will be available at [http://localhost:8000](http://localhost:8000)

---

## Frontend Setup (React + Vite)

1. **Navigate to the frontend directory:**
   ```sh
   cd auth-frontend
   ```
2. **Install dependencies:**
   ```sh
   npm install
   ```
3. **Start the development server:**
   ```sh
   npm run dev
   ```
   The frontend will be available at [http://localhost:5173](http://localhost:5173)

---

## API Endpoints

### Authentication Endpoints
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/forgot-password` - Request password reset
- `POST /api/reset-password` - Reset password with token
- `GET /api/healthz` - Health check

### Student Management Endpoints
- `GET /api/students` - Get all students or filter by course/ID
- `POST /api/students` - Add a new student
- `PUT /api/students/{studentId}` - Update student grade for a course
- `DELETE /api/students/{studentId}` - Delete a student

### Student Data Structure
```json
{
  "id": 12345,
  "name": "John Doe",
  "age": 20,
  "courses": [
    {
      "code": "CS101",
      "name": "Introduction to Programming",
      "grade": "A"
    }
  ],
  "contact": {
    "email": "john@example.com",
    "phone": "+1234567890"
  }
}
```

---

## Environment Variables

Create a `.env` file in the `app/` directory with the following variables:

```
# MongoDB
MONGODB_URI=mongodb://localhost:27017/your-db

# JWT Secret
SECRET_KEY=your_secret_key

# Email (SMTP) settings
MAIL_FROM=your@email.com
MAIL_SERVER=smtp.yourprovider.com
MAIL_PORT=587
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=your_email_password
```

---

## Development Workflow
- Start the backend server first (FastAPI on port 8000)
- Then start the frontend dev server (Vite/React on port 5173)
- The frontend is configured to communicate with the backend at `http://localhost:8000`
- Use the provided endpoints for authentication, registration, password reset, and student management

### Student Management Workflow
1. **Login** to access the dashboard
2. **Navigate** to Students Dashboard
3. **Add Students** with course enrollments and grades
4. **Filter Students** by course to view specific enrollments
5. **Edit Grades** for individual courses
6. **Delete Students** when needed

---

## Notes
- Do **not** commit your `.env` file or any secrets to version control.
- For production, update CORS settings and environment variables as needed.
- Health check endpoint: `GET /api/healthz` on the backend.
- Student data is stored in `students_data.json` - ensure proper backups.
- For any issues, check logs in the backend terminal for errors.
- The system supports multiple courses per student with individual grade tracking. 