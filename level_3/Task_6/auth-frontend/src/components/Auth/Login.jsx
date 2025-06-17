import React, { useState } from 'react';
import {
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  FormControlLabel,
  Checkbox,
  Link,
} from '@mui/material';
import { loginUser } from '../../api/auth';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [form, setForm] = useState({
    Email: '',
    Password: '',
  });
  const [rememberMe, setRememberMe] = useState(false);
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};

    // Required field validation
    if (!form.Email.trim()) {
      newErrors.Email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(form.Email)) {
      newErrors.Email = 'Please enter a valid email address';
    }

    if (!form.Password) {
      newErrors.Password = 'Password is required';
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

  const handleLogin = async () => {
    setSuccess('');
    
    if (!validateForm()) {
      return;
    }

    try {
      const response = await loginUser(form);
      const token = response.AccessToken;

      if (rememberMe) {
        localStorage.setItem('token', token);
      } else {
        sessionStorage.setItem('token', token);
      }

      setSuccess('Login successful!');
      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
    } catch (err) {
      setErrors({ submit: err.response?.data?.detail || 'Login failed' });
    }
  };

  return (
    <Box sx={{ width: 400, mx: 'auto', mt: 5 }}>
      <Typography variant="h5" gutterBottom>
        Login
      </Typography>

      {errors.submit && <Alert severity="error" sx={{ mb: 2 }}>{errors.submit}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

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

      <FormControlLabel
        control={
          <Checkbox
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
          />
        }
        label="Remember me"
      />

      <Box textAlign="right" mb={1}>
        <Link href="/forgot-password" underline="hover">
          Forgot Password?
        </Link>
      </Box>

      <Button
        variant="contained"
        color="secondary"
        fullWidth
        sx={{ mt: 1 }}
        onClick={handleLogin}
      >
        Login
      </Button>
    </Box>
  );
};

export default LoginForm;
