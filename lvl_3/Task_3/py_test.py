import pytest
import copy
import os
import json

# Import functions to test from StudentManager
from json_handler import (
    LoadJsonFile,
    SaveJsonFile,
    AddStudent,
    RemoveStudent,
    UpdateStudentGrade,
    GetStudentDetails,
    GetCourseStudents
)

@pytest.fixture
def SampleData():
    """
    Load a fresh copy of the student data from file for each test.
    This ensures tests don't interfere with each other.
    """
    with open("students_data.json") as f:
        data = json.load(f)
    return copy.deepcopy(data)

class TestStudentManager:
    """
    A test class containing all test cases for the StudentManager functions.
    """

    def TestLoadJsonFile(self):
        """Test loading JSON from file."""
        data = LoadJsonFile("students_data.json")
        assert "students" in data
        assert isinstance(data["students"], list)

    def test_AddStudent(self, SampleData):
        """Test adding a new student."""
        newStudent = {
            "id": 3,
            "name": "Nihil  S",
            "age": 21,
            "courses": [
                {"code": "CS202", "name": "Data Structures", "grade": "A"},
            ],
            "contact": {
                "email": "nihil@example.com",
                "phone": "111-222-3333"
            }
        }
        AddStudent(SampleData, newStudent)
        assert any(s['id'] == 3 for s in SampleData['students'])

    def test_AddExistingStudentRaises(self, SampleData):
        """Test that adding a student with an existing ID raises an error."""
        with pytest.raises(ValueError, match="already exists"):
            AddStudent(SampleData, SampleData['students'][0])

    def test_RemoveStudent(self, SampleData):
        """Test removing a student by ID."""
        RemoveStudent(SampleData, 2)
        assert all(s['id'] != 2 for s in SampleData['students'])

    def test_RemoveInvalidStudentRaises(self, SampleData):
        """Test that removing a non-existent student raises an error."""
        with pytest.raises(ValueError, match="not found"):
            RemoveStudent(SampleData, 999)

    def test_UpdateStudentGrade(self, SampleData):
        """Test updating a grade for a specific student and course."""
        UpdateStudentGrade(SampleData, 1, "CS101", "A+")
        student = next(s for s in SampleData['students'] if s['id'] == 1)
        course = next(c for c in student['courses'] if c['code'] == "CS101")
        assert course['grade'] == "A+"

    def test_UpdateInvalidCourseRaises(self, SampleData):
        """Test that updating a non-existent course raises an error."""
        with pytest.raises(ValueError, match="not found"):
            UpdateStudentGrade(SampleData, 1, "XX999", "B")

    def test_GetStudentDetails(self, SampleData):
        """Test fetching details of an existing student."""
        student = GetStudentDetails(SampleData, 2)
        assert student['name'] == "Emma Wilson"

    def test_GetStudentDetailsInvalidRaises(self, SampleData):
        """Test that fetching a non-existent student's details raises an error."""
        with pytest.raises(ValueError, match="not found"):
            GetStudentDetails(SampleData, 999)

    def test_GetCourseStudents(self, SampleData):
        """Test fetching all students enrolled in a course."""
        students = GetCourseStudents(SampleData, "CS101")
        assert len(students) >= 1
        assert any(s['name'] == "John Smith" for s in students)

    def test_GetCourseStudentsInvalidRaises(self, SampleData):
        """Test that requesting students from a non-existent course raises an error."""
        with pytest.raises(ValueError, match="No students found"):
            GetCourseStudents(SampleData, "ZZZ999")

    def test_SaveAndReloadJson(self, tmp_path, SampleData):
        """Test saving data to JSON and loading it back correctly."""
        filePath = tmp_path / "TestOutput.json"
        SaveJsonFile(str(filePath), SampleData)
        assert os.path.exists(filePath)
        reloaded = LoadJsonFile(str(filePath))
        assert reloaded == SampleData
