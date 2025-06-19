import json
from typing import Dict, List, Union, Any
import logging

def LoadJsonFile(filename: str) -> Dict[str, Any]:
    """
    Load and parse JSON data from a file.
    Raises errors if the file is not found or contains invalid JSON.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File '{filename}' not found.")
        raise FileNotFoundError(f"File '{filename}' not found.")
    except json.JSONDecodeError:
        logging.error(f"File '{filename}' contains invalid JSON.")
        raise ValueError(f"File '{filename}' contains invalid JSON.")

def SaveJsonFile(filename: str, data: Dict[str, Any]) -> None:
    """
    Save dictionary data back to a JSON file with pretty formatting (indentation).
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def AddStudent(data: Dict[str, Any], studentInfo: Dict[str, Any]) -> None:
    """
    Add a new student to the list of students.
    Ensures that studentInfo includes all required fields and ID is unique.
    """
    requiredKeys = {'id', 'name', 'age', 'courses', 'contact'}
    if not requiredKeys.issubset(studentInfo.keys()):
        logging.error(f"Student info missing required fields: {requiredKeys}")
        raise ValueError(f"Student info missing required fields: {requiredKeys}")

    # Prevent duplicate IDs
    if any(student['id'] == studentInfo['id'] for student in data.get('students', [])):
        logging.error(f"Student with ID {studentInfo['id']} already exists.")
        raise ValueError(f"Student with ID {studentInfo['id']} already exists.")

    data.setdefault('students', []).append(studentInfo)

def RemoveStudent(data: Dict[str, Any], studentId: int) -> None:
    """
    Remove a student from the list using their unique ID.
    Raises an error if student is not found.
    """
    students = data.get('students', [])
    for i, student in enumerate(students):
        if student['id'] == studentId:
            del students[i]
            return
    logging.error(f"Student with ID {studentId} not found.")
    raise ValueError(f"Student with ID {studentId} not found.")

def UpdateStudentGrade(data: Dict[str, Any], studentId: int, courseCode: str, newGrade: str) -> None:
    """
    Update the grade for a specific course of a given student.
    Raises an error if the student or course is not found.
    """
    for student in data.get('students', []):
        if student['id'] == studentId:
            for course in student['courses']:
                if course['code'] == courseCode:
                    course['grade'] = newGrade
                    return
            logging.error(f"Course with code '{courseCode}' not found for student ID {studentId}.")
            raise ValueError(f"Course with code '{courseCode}' not found for student ID {studentId}.")
    logging.error(f"Student with ID {studentId} not found.")
    raise ValueError(f"Student with ID {studentId} not found.")

def GetStudentDetails(data: Dict[str, Any], studentId: int) -> Dict[str, Any]:
    """
    Retrieve full information of a student by their ID.
    """
    for student in data.get('students', []):
        if student['id'] == studentId:
            return student
    logging.error(f"Student with ID {studentId} not found.")
    raise ValueError(f"Student with ID {studentId} not found.")

def GetCourseStudents(data: Dict[str, Any], courseCode: str) -> List[Dict[str, Union[str, int]]]:
    """
    Get a list of students who are enrolled in a specific course.
    Returns a list of dictionaries containing student names and IDs.
    Raises error if no students are found in the course.
    """
    enrolledStudents = []
    for student in data.get('students', []):
        for course in student['courses']:
            if course['code'] == courseCode:
                enrolledStudents.append({'id': student['id'], 'name': student['name']})
                break  # No need to check more courses for this student

    if not enrolledStudents:
        logging.error(f"No students found enrolled in course '{courseCode}'.")
        raise ValueError(f"No students found enrolled in course '{courseCode}'.")

    return enrolledStudents
