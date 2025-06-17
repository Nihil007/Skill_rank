import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/auth',
});

export const registerUser = async (data) => {
  const res = await API.post('/register', data);
  return res.data;
};

export const loginUser = async (data) => {
  const res = await API.post('/login', data);
  return res.data;
};

export const sendResetEmail = async (email) => {
  const res = await API.post('/reset-password', { Email: email });
  return res.data;
};

export const confirmResetPassword = async ({ token, password }) => {
  const res = await API.post('/confirm-reset', {
    Token: token,
    NewPassword: password,
    ConfirmPassword: password, // optional if your backend expects confirmation
  });
  return res.data;
};
