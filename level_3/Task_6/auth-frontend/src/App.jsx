import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RegisterForm from './components/Auth/RegisterForm';
import Login from './components/Auth/Login';
import Home from './components/Home';
import Dashboard from './components/Dashboard';
import ResetPassword from './components/Auth/ResetPass';
import ForgotPassword from './components/auth/ForgotPass';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        {/* Add login route later */}
      </Routes>
    </Router>
  );
}

export default App;
