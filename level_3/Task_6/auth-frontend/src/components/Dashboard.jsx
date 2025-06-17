import React, { useEffect, useState } from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [userInfo, setUserInfo] = useState({ email: '', name: '' });
  const navigate = useNavigate();

  useEffect(() => {
    const token =
      localStorage.getItem('token') || sessionStorage.getItem('token');
    if (!token) {
      navigate('/login');
    } else {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        setUserInfo({
          email: payload.sub,
          name: payload.name || 'User',
        });
      } catch (err) {
        console.error('Invalid token');
        navigate('/login');
      }
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    sessionStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 10 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Welcome to the Dashboard
        </Typography>

        <Typography variant="body1" sx={{ mb: 1 }}>
          <strong>Name:</strong> {userInfo.name}
        </Typography>

        <Typography variant="body1" sx={{ mb: 2 }}>
          <strong>Email:</strong> {userInfo.email}
        </Typography>

        <Typography variant="h6" gutterBottom>
          Project Workflow
        </Typography>

        <Typography variant="body2" sx={{ whiteSpace: 'pre-line', mb: 3 }}>
          {`1. User registers or logs in to the system.
2. Authenticated users receive a secure token.
3. Users access protected pages like the Dashboard.
4. If password is forgotten, a reset link is emailed.
5. Clicking the link opens the reset password page.
6. After resetting, users are redirected to login.
7. Logout clears session/token and returns to login.`}
        </Typography>

        <Button variant="contained" color="secondary" onClick={handleLogout}>
          Logout
        </Button>
      </Paper>
    </Box>
  );
};

export default Dashboard;
