// services/auth.js
import axios from 'axios';

const token = localStorage.getItem('token');

axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

export const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const login = async (username, password) => {
  try {
    const response = await axiosInstance.post('/login', {
      username,
      password,
    });
    if (response.data.success === false) {
      return response;
    }
    const accessToken = response.data.accessToken;
    localStorage.setItem('token', accessToken);
    localStorage.setItem('username', username);
    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  delete axiosInstance.defaults.headers.common['Authorization'];
};

export const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  return token !== null;
};

