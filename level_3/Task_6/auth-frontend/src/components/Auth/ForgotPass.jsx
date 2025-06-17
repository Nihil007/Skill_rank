import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Alert,
} from '@mui/material';
import { sendResetEmail } from '../../api/auth';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setMessage('');
    setError('');
    try {
      const response = await sendResetEmail(email);
      setMessage(response.detail || 'Reset link sent!');
    } catch (err) {
      // Extract error message safely
      const errorDetail = err.response?.data?.detail;

      if (Array.isArray(errorDetail)) {
        // If it's a list of validation errors
        setError(errorDetail.map(e => e.msg).join(', '));
      } else {
        setError(errorDetail || 'Failed to send reset link');
      }
    }
  };

  return (
    <Box sx={{ width: 400, mx: 'auto', mt: 5 }}>
      <Typography variant="h5" gutterBottom>
        Forgot Password
      </Typography>
      {message && <Alert severity="success">{message}</Alert>}
      {error && <Alert severity="error">{error}</Alert>}
      <TextField
        label="Email"
        fullWidth
        margin="normal"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <Button variant="contained" color="secondary" fullWidth sx={{ mt: 2 }} onClick={handleSubmit}>
        Send Reset Link
      </Button>
    </Box>
  );
};

export default ForgotPassword;
