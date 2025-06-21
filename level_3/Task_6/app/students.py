# Import necessary FastAPI and utility modules
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import logging

# Import student-related functions from json_handler
from json_handler import (
    LoadJsonFile,
    SaveJsonFile,
    AddStudent,
    RemoveStudent,
    UpdateStudentGrade,
    GetStudentDetails,
    GetCourseStudents
)

# Create a new API router for student routes
router = APIRouter()

# Set up a logger for this module
logger = logging.getLogger(__name__)

# Path to the JSON file that stores student data
DATA_FILE = "students_data.json"

# Model for updating a student's course grade
class CourseGradeUpdate(BaseModel):
    courseCode: str
    newGrade: str

# Model for a student (used in POST request)
class StudentModel(BaseModel):
    id: int
    name: str
    age: int
    courses: list
    contact: dict

# POST - Add a new student to the system
@router.post("/api/students")
def CreateStudent(student: StudentModel):
    try:
        # Load existing student data
        data = LoadJsonFile(DATA_FILE)

        # Add new student to the data
        AddStudent(data, student.dict())

        # Save updated data back to the file
        SaveJsonFile(DATA_FILE, data)

        # Return success message
        return {"message": "Student added successfully."}

    except Exception as e:
        # Log and return any error that occurs
        logger.error(f"Error adding student: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# GET - Retrieve a student by ID, list students by course, or get all students
@router.get("/api/students")
def GetStudents(studentId: Optional[int] = None, courseCode: Optional[str] = None):
    try:
        # Load student data from the file
        data = LoadJsonFile(DATA_FILE)

        # Return individual student details if ID is provided
        if studentId is not None:
            student = GetStudentDetails(data, studentId)
            return student

        # Return list of students enrolled in a course if course code is provided
        elif courseCode is not None:
            students = GetCourseStudents(data, courseCode)
            return students

        # Return all students if no parameters provided
        else:
            return {"students": data.get("students", [])}

    except Exception as e:
        # Log and return any error that occurs
        logger.error(f"Error retrieving students: {e}")
        raise HTTPException(status_code=404, detail=str(e))

# PUT - Update a student's grade for a course
@router.put("/api/students/{studentId}")
def UpdateGrade(studentId: int, gradeUpdate: CourseGradeUpdate):
    try:
        # Load student data
        data = LoadJsonFile(DATA_FILE)

        # Update the student's grade for the given course
        UpdateStudentGrade(data, studentId, gradeUpdate.courseCode, gradeUpdate.newGrade)

        # Save the updated data
        SaveJsonFile(DATA_FILE, data)

        # Return success message
        return {"message": "Student grade updated successfully."}

    except Exception as e:
        # Log and return any error that occurs
        logger.error(f"Error updating student grade: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# DELETE - Remove a student from the system
@router.delete("/api/students/{studentId}")
def DeleteStudent(studentId: int):
    try:
        # Load student data
        data = LoadJsonFile(DATA_FILE)

        # Remove the student by ID
        RemoveStudent(data, studentId)

        # Save the updated data
        SaveJsonFile(DATA_FILE, data)

        # Return success message
        return {"message": "Student removed successfully."}

    except Exception as e:
        # Log and return any error that occurs
        logger.error(f"Error deleting student: {e}")
        raise HTTPException(status_code=404, detail=str(e))
