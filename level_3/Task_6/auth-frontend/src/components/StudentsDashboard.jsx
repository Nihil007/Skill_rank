import React, { useEffect, useState } from 'react';
import {
  Box, Typography, Button, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, 
  Dialog, DialogTitle, DialogContent, DialogActions, TextField, Select, MenuItem, InputLabel, 
  FormControl, Alert, Chip, Card, CardContent, Grid, Snackbar, CircularProgress,
  FormGroup, FormControlLabel, Checkbox, Divider
} from '@mui/material';
import { getStudents, addStudent, editStudentGrade, deleteStudent } from '@/api/students';

const StudentsDashboard = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [openAdd, setOpenAdd] = useState(false);
  const [openEdit, setOpenEdit] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [grade, setGrade] = useState('');
  const [filterCourse, setFilterCourse] = useState('');
  const [addForm, setAddForm] = useState({
    id: '', name: '', age: '', contact: { email: '', phone: '' }
  });
  const [selectedCourses, setSelectedCourses] = useState({});
  const [courseGrades, setCourseGrades] = useState({});

  // Predefined courses
  const availableCourses = [
    { code: 'CS101', name: 'Introduction to Programming' },
    { code: 'MT102', name: 'Mathematics' },
    { code: 'PH201', name: 'Physics' },
    { code: 'CS202', name: 'Data Structures' },
    { code: 'EN101', name: 'English Literature' },
    { code: 'CH101', name: 'Chemistry' }
  ];

  const fetchStudents = async (filter = '') => {
    setLoading(true);
    setError('');
    try {
      // Always fetch all students
      const data = await getStudents();
      const allStudents = data.students || [];
      
      // If filter is applied, filter students who have the selected course
      if (filter) {
        const filteredStudents = allStudents.filter(student => 
          student.courses?.some(course => course.code === filter)
        );
        setStudents(filteredStudents);
      } else {
        setStudents(allStudents);
      }
    } catch (err) {
      setError('Failed to fetch students: ' + (err.response?.data?.detail || err.message));
      setStudents([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchStudents(filterCourse);
  }, [filterCourse]);

  const handleOpenAdd = () => {
    setAddForm({ id: '', name: '', age: '', contact: { email: '', phone: '' } });
    setSelectedCourses({});
    setCourseGrades({});
    setOpenAdd(true);
  };
  const handleCloseAdd = () => setOpenAdd(false);

  const handleCourseChange = (courseCode, checked) => {
    setSelectedCourses(prev => ({
      ...prev,
      [courseCode]: checked
    }));

    if (!checked) {
      setCourseGrades(prev => {
        const newGrades = { ...prev };
        delete newGrades[courseCode];
        return newGrades;
      });
    }
  };
  
  const handleGradeChange = (courseCode, newGrade) => {
    setCourseGrades(prev => ({
      ...prev,
      [courseCode]: newGrade
    }));
  };

  const handleAddStudent = async () => {
    try {
      if (!addForm.id || !addForm.name || !addForm.age) {
        setError('Please fill in all required fields');
        return;
      }

      const selectedCourseCodes = Object.keys(selectedCourses).filter(code => selectedCourses[code]);
      if (selectedCourseCodes.length === 0) {
        setError('Please select at least one course');
        return;
      }

      const courses = selectedCourseCodes.map(code => {
        const course = availableCourses.find(c => c.code === code);
        return {
          code: course.code,
          name: course.name,
          grade: courseGrades[code] || 'N/A'
        };
      });

      await addStudent({
        id: Number(addForm.id),
        name: addForm.name,
        age: Number(addForm.age),
        courses,
        contact: addForm.contact
      });
      setOpenAdd(false);
      setSuccess('Student added successfully!');
      fetchStudents(filterCourse);
    } catch (err) {
      setError('Failed to add student: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleOpenEdit = (student) => {
    setSelectedStudent(student);
    setOpenEdit(true);
    setSelectedCourse('');
    setGrade('');
  };
  const handleCloseEdit = () => setOpenEdit(false);

  const handleEditGrade = async () => {
    try {
      if (!selectedCourse || !grade) {
        setError('Please select a course and enter a grade');
        return;
      }
      await editStudentGrade(selectedStudent.id, selectedCourse, grade);
      setOpenEdit(false);
      setSuccess('Grade updated successfully!');
      fetchStudents(filterCourse);
    } catch (err) {
      setError('Failed to update grade: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDelete = async (studentId) => {
    if (!window.confirm('Are you sure you want to delete this student?')) return;
    try {
      await deleteStudent(studentId);
      setSuccess('Student deleted successfully!');
      fetchStudents(filterCourse);
    } catch (err) {
      setError('Failed to delete student: ' + (err.response?.data?.detail || err.message));
    }
  };

  const getUniqueCourses = () => {
    // Always return all available courses, not just from filtered students
    return availableCourses.map(course => course.code);
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', mt: 4, mb: 4, px: 2 }}>
      <Card elevation={3}>
        <CardContent>
          <Typography variant="h4" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
            Students Dashboard
          </Typography>
          
          <Grid container spacing={2} sx={{ mb: 3 }} alignItems="center">
            <Grid item xs={12} sm={4}>
              <Button 
                variant="contained" 
                fullWidth
                onClick={handleOpenAdd}
                sx={{ py: 1.5, fontWeight: 'bold' }}
              >
                + Add Student
              </Button>
            </Grid>
            <Grid item xs={12} sm={5}>
              <FormControl fullWidth>
                <InputLabel >Filter by Course</InputLabel>
                <Select
                  value={filterCourse}
                  label="Filter by Course"
                  onChange={e => setFilterCourse(e.target.value)}
                  sx={{ 
                    minWidth: 160,
                    '& .MuiSelect-select': {
                      py: 1.5,
                      fontSize: '1rem'
                    }
                  }}
                >
                  <MenuItem value="">All Students</MenuItem>
                  {getUniqueCourses().map(course => (
                    <MenuItem key={course} value={course}>
                      {course} 
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, textAlign: 'right' }}>
                <Typography variant="body2" color="text.secondary">
                  Total Students: {students.length}
                </Typography>
                {filterCourse && (
                  <Chip 
                    label={`Filtering: ${filterCourse}`}
                    color="secondary"
                    size="small"
                    onDelete={() => setFilterCourse('')}
                  />
                )}
              </Box>
            </Grid>
          </Grid>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
              {error}
            </Alert>
          )}

          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : students.length === 0 ? (
            <Alert severity="info">
              No students found. {filterCourse ? `No students enrolled in ${filterCourse}` : 'Add some students to get started!'}
            </Alert>
          ) : (
            <TableContainer component={Paper} elevation={1}>
              <Table>
                <TableHead>
                  <TableRow sx={{ backgroundColor: 'primary.main' }}>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>ID</TableCell>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Name</TableCell>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Age</TableCell>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Courses</TableCell>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Contact</TableCell>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {students.map((student) => (
                    <TableRow key={student.id} hover>
                      <TableCell>{student.id}</TableCell>
                      <TableCell sx={{ fontWeight: 'medium' }}>{student.name}</TableCell>
                      <TableCell>{student.age}</TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {student.courses?.map((course, idx) => (
                            <Chip 
                              key={idx}
                              label={`${course.code}: ${course.grade}`}
                              size="small"
                              color={
                                filterCourse && course.code === filterCourse 
                                  ? 'secondary' 
                                  : course.grade?.toUpperCase().startsWith('A') 
                                    ? 'success' 
                                    : course.grade?.toUpperCase().startsWith('B')
                                      ? 'primary' 
                                      : 'default'
                              }
                              variant={filterCourse && course.code === filterCourse ? 'filled' : 'outlined'}
                              sx={{
                                fontWeight: filterCourse && course.code === filterCourse ? 'bold' : 'normal',
                                border: filterCourse && course.code === filterCourse ? '2px solid' : '1px solid'
                              }}
                            />
                          ))}
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{student.contact?.email}</Typography>
                        <Typography variant="body2" color="text.secondary">{student.contact?.phone}</Typography>
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Button 
                            size="small" 
                            variant="outlined" 
                            onClick={() => handleOpenEdit(student)}
                            sx={{ minWidth: 'auto' }}
                          >
                            Edit Grade
                          </Button>
                          <Button 
                            size="small" 
                            variant="outlined" 
                            color="error"
                            onClick={() => handleDelete(student.id)}
                            sx={{ minWidth: 'auto' }}
                          >
                            Delete
                          </Button>
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </CardContent>
      </Card>

      {/* Add Student Dialog */}
      <Dialog open={openAdd} onClose={handleCloseAdd} maxWidth="lg" fullWidth>
        <DialogTitle>Add New Student</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <Grid container spacing={4}>
            {/* Left Column: Personal Details */}
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Personal Details
              </Typography>
              <Divider sx={{ mb: 3 }} />
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField 
                    label="Student ID" 
                    value={addForm.id} 
                    onChange={e => setAddForm(f => ({ ...f, id: e.target.value }))}
                    fullWidth
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField 
                    label="Age" 
                    value={addForm.age} 
                    onChange={e => setAddForm(f => ({ ...f, age: e.target.value }))}
                    fullWidth
                    required
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField 
                    label="Full Name" 
                    value={addForm.name} 
                    onChange={e => setAddForm(f => ({ ...f, name: e.target.value }))}
                    fullWidth
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField 
                    label="Email" 
                    value={addForm.contact.email} 
                    onChange={e => setAddForm(f => ({ ...f, contact: { ...f.contact, email: e.target.value } }))}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField 
                    label="Phone" 
                    value={addForm.contact.phone} 
                    onChange={e => setAddForm(f => ({ ...f, contact: { ...f.contact, phone: e.target.value } }))}
                    fullWidth
                  />
                </Grid>
              </Grid>
            </Grid>

            {/* Right Column: Courses & Grades */}
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Courses & Grades
              </Typography>
              <Divider sx={{ mb: 3 }} />
              <FormGroup>
                {availableCourses.map((course) => (
                  <Grid container key={course.code} alignItems="center" spacing={2} sx={{ mb: 1 }}>
                    <Grid item xs={12} sm={7}>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={selectedCourses[course.code] || false}
                            onChange={(e) => handleCourseChange(course.code, e.target.checked)}
                          />
                        }
                        label={`${course.code} - ${course.name}`}
                      />
                    </Grid>
                    <Grid item xs={12} sm={5}>
                      {selectedCourses[course.code] && (
                        <TextField
                          label="Grade"
                          variant="outlined"
                          size="small"
                          fullWidth
                          value={courseGrades[course.code] || ''}
                          onChange={(e) => handleGradeChange(course.code, e.target.value)}
                        />
                      )}
                    </Grid>
                  </Grid>
                ))}
              </FormGroup>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseAdd}>Cancel</Button>
          <Button onClick={handleAddStudent} variant="contained">Add Student</Button>
        </DialogActions>
      </Dialog>

      {/* Edit Grade Dialog */}
      <Dialog open={openEdit} onClose={handleCloseEdit} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Student Grade</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Student: <strong>{selectedStudent?.name}</strong>
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Select Course</InputLabel>
                <Select
                  value={selectedCourse}
                  label="Select Course"
                  onChange={e => setSelectedCourse(e.target.value)}
                >
                  {selectedStudent?.courses?.map((course, idx) => (
                    <MenuItem key={idx} value={course.code}>
                      {course.code} - {course.name} (Current: {course.grade})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField 
                label="New Grade" 
                value={grade} 
                onChange={e => setGrade(e.target.value)}
                fullWidth
                placeholder="A, B, C, D, F"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseEdit}>Cancel</Button>
          <Button onClick={handleEditGrade} variant="contained">Update Grade</Button>
        </DialogActions>
      </Dialog>

      {/* Success Snackbar */}
      <Snackbar 
        open={!!success} 
        autoHideDuration={4000} 
        onClose={() => setSuccess('')}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={() => setSuccess('')} severity="success">
          {success}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default StudentsDashboard; 