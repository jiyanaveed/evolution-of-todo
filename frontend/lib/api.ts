import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: adds Bearer token to every request
api.interceptors.request.use((config) => {
  // Try to get Better Auth token from localStorage for API requests
  // Only access localStorage on the client side
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('better-auth.session_token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Response interceptor: stores new tokens from responses
api.interceptors.response.use((response) => {
  // Store token from response if present
  if (typeof window !== 'undefined' && response.data?.token) {
    localStorage.setItem('better-auth.session_token', response.data.token);
  }
  return response;
}, (error) => {
  // Handle global error responses here
  console.error('API Error:', error);

  // Handle 401 Unauthorized errors
  if (typeof window !== 'undefined' && error.response && error.response.status === 401) {
    // Clear token and redirect to login page
    localStorage.removeItem('better-auth.session_token');
    window.location.href = '/login';
  }

  return Promise.reject(error);
});

export default api;