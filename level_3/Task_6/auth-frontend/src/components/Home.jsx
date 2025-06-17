import { Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <Stack spacing={3} alignItems="center" justifyContent="center" height="100vh">
      <Typography variant="h4" fontWeight="bold">
        Welcome to the Auth System
      </Typography>
      <Stack direction="row" spacing={2}>
        <Button variant="contained" color="secondary" component={Link} to="/register">
          Register
        </Button>
        <Button variant="outlined" color="secondary" component={Link} to="/login">
          Login
        </Button>
      </Stack>
    </Stack>
  );
};

export default Home;
