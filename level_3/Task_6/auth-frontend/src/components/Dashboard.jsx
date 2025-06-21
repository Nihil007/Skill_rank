import React, { useEffect, useState } from 'react';
import { 
  Box, Typography, Button, Paper, Grid, Avatar, 
  Divider, Container
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import SchoolIcon from '@mui/icons-material/School';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

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

  const getInitials = (name) => {
    if (!name) return '';
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4, p: { xs: 2, md: 4 } }}>
      <Grid container spacing={4}>
        {/* Left Sidebar - Profile & Actions */}
        <Grid item xs={12} md={4}>
          <Paper elevation={0} variant="outlined" sx={{ borderRadius: 4, p: 3, height: '100%' }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
              <Avatar
                sx={{
                  width: 100,
                  height: 100,
                  bgcolor: 'primary.main',
                  color: 'white',
                  fontSize: '2.5rem',
                  mb: 2
                }}
              >
                {getInitials(userInfo.name)}
              </Avatar>
              <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                {userInfo.name}
              </Typography>
              <Typography variant="body1" color="text.secondary">
                {userInfo.email}
              </Typography>
            </Box>

            <Divider sx={{ my: 3 }} />
            
            <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
              <Button
                variant="outlined"
                color="error"
                fullWidth
                startIcon={<ExitToAppIcon />}
                onClick={handleLogout}
                sx={{ fontWeight: 'bold', borderRadius: 2 }}
              >
                Logout
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Main Content */}
        <Grid item xs={12} md={8}>
          <Paper elevation={0} variant="outlined" sx={{ borderRadius: 4, p: 4, height: '100%' }}>
            <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mb: 1 }}>
              Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Welcome to your student management portal. Use the actions on the left to get started.
            </Typography>
            
            <Divider sx={{ my: 3 }} />
            
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                Getting Started
              </Typography>
              <Paper variant="outlined" sx={{ borderRadius: 3, p: 3, display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderStyle: 'dashed' }}>
                <Box>
                  <Typography sx={{ fontWeight: 'medium' }}>Navigate to the student section</Typography>
                  <Typography variant="body2" color="text.secondary">Click the button to view and manage all student data.</Typography>
                </Box>
                <Button 
                  variant="contained" 
                  disableElevation
                  onClick={() => navigate('/dashboard/students')}
                  endIcon={<ArrowForwardIcon />}
                >
                  Go
                </Button>
              </Paper>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
