# Skill Rank - Task 6

This project is a full-stack authentication system with a FastAPI backend and a React (Vite) frontend. It supports user registration, login, password reset via email, and a protected dashboard.

---

## Table of Contents
- [Project Structure](#project-structure)
- [Backend Setup (FastAPI)](#backend-setup-fastapi)
- [Frontend Setup (React + Vite)](#frontend-setup-react--vite)
- [Environment Variables](#environment-variables)
- [Development Workflow](#development-workflow)
- [Notes](#notes)

---

## Project Structure

```
Task_6/
  app/                # FastAPI backend
  auth-frontend/      # React frontend
```

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
- Use the provided endpoints for authentication, registration, and password reset

---

## Notes
- Do **not** commit your `.env` file or any secrets to version control.
- For production, update CORS settings and environment variables as needed.
- Health check endpoint: `GET /api/healthz` on the backend.
- For any issues, check logs in the backend terminal for errors. 