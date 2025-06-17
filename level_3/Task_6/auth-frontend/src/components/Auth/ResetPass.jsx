import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Alert,
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import { confirmResetPassword } from '../../api/auth';

const ResetPassword = () => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const query = new URLSearchParams(useLocation().search);
  const token = query.get('token');

  useEffect(() => {
    if (!token) {
      setError('Invalid or missing token');
    }
  }, [token]);

  const handleSubmit = async () => {
    setError('');
    setMessage('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await confirmResetPassword({ token, password });
      setMessage(response.Message || 'Password has been reset');
      setTimeout(() => navigate('/login'), 1500);
    } catch (err) {
      const errorDetail = err.response?.data?.detail;
      setError(typeof errorDetail === 'string' ? errorDetail : 'Failed to reset password');
    }
  };

  return (
    <Box sx={{ width: 400, mx: 'auto', mt: 5 }}>
      <Typography variant="h5" gutterBottom>Reset Password</Typography>
      {error && <Alert severity="error">{error}</Alert>}
      {message && <Alert severity="success">{message}</Alert>}

      <TextField
        label="New Password"
        type="password"
        fullWidth
        margin="normal"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <TextField
        label="Confirm New Password"
        type="password"
        fullWidth
        margin="normal"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
      />
      <Button
        variant="contained"
        color="secondary"
        fullWidth
        sx={{ mt: 2 }}
        onClick={handleSubmit}
        disabled={!token}
      >
        Reset Password
      </Button>
    </Box>
  );
};

export default ResetPassword;
