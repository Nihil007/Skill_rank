import React, { useState } from 'react';
import { TextField, Button, Typography, Box, Alert } from '@mui/material';
import { registerUser } from '../../api/auth';
import { useNavigate } from 'react-router-dom';

const RegisterForm = () => {
  const [form, setForm] = useState({
    Username: '',
    Email: '',
    Password: '',
    ConfirmPassword: '',
  });
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};

    // Required field validation
    if (!form.Username.trim()) {
      newErrors.Username = 'Username is required';
    }

    if (!form.Email.trim()) {
      newErrors.Email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(form.Email)) {
      newErrors.Email = 'Please enter a valid email address';
    }

    if (!form.Password) {
      newErrors.Password = 'Password is required';
    } else if (form.Password.length < 6) {
      newErrors.Password = 'Password must be at least 6 characters long';
    }

    if (!form.ConfirmPassword) {
      newErrors.ConfirmPassword = 'Please confirm your password';
    } else if (form.Password !== form.ConfirmPassword) {
      newErrors.ConfirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }
  };

  const handleSubmit = async () => {
    setSuccess('');
    
    if (!validateForm()) {
      return;
    }

    try {
      const response = await registerUser(form);
      setSuccess(response.Message);

      // Redirect to login after short delay
      setTimeout(() => {
        navigate('/login');
      }, 1000);
    } catch (err) {
      setErrors({ submit: err.response?.data?.detail || 'Registration failed' });
    }
  };

  return (
    <Box sx={{ width: 400, mx: 'auto', mt: 5 }}>
      <Typography variant="h5" gutterBottom>Register</Typography>
      {errors.submit && <Alert severity="error" sx={{ mb: 2 }}>{errors.submit}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
      
      <TextField
        label="Username"
        name="Username"
        fullWidth
        margin="normal"
        value={form.Username}
        onChange={handleChange}
        error={!!errors.Username}
        helperText={errors.Username}
        required
      />
      <TextField
        label="Email"
        name="Email"
        type="email"
        fullWidth
        margin="normal"
        value={form.Email}
        onChange={handleChange}
        error={!!errors.Email}
        helperText={errors.Email}
        required
      />
      <TextField
        label="Password"
        name="Password"
        type="password"
        fullWidth
        margin="normal"
        value={form.Password}
        onChange={handleChange}
        error={!!errors.Password}
        helperText={errors.Password}
        required
      />
      <TextField
        label="Confirm Password"
        name="ConfirmPassword"
        type="password"
        fullWidth
        margin="normal"
        value={form.ConfirmPassword}
        onChange={handleChange}
        error={!!errors.ConfirmPassword}
        helperText={errors.ConfirmPassword}
        required
      />
      <Button 
        variant="contained" 
        color="secondary" 
        fullWidth 
        sx={{ mt: 2 }} 
        onClick={handleSubmit}
      >
        Register
      </Button>
    </Box>
  );
};

export default RegisterForm;
