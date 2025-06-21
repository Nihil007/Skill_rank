import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Get students (optionally by courseCode or studentId, or all students if no params)
export const getStudents = async (params = {}) => {
  const res = await API.get('/students', { params });
  return res.data;
};

// Add a new student
export const addStudent = async (student) => {
  const res = await API.post('/students', student);
  return res.data;
};

// Edit a student's grade for a course
export const editStudentGrade = async (studentId, courseCode, newGrade) => {
  const res = await API.put(`/students/${studentId}`, { courseCode, newGrade });
  return res.data;
};

// Delete a student
export const deleteStudent = async (studentId) => {
  const res = await API.delete(`/students/${studentId}`);
  return res.data;
}; 