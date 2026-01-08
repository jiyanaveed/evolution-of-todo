'use client';

import React, { createContext, useContext, ReactNode, useEffect, useState } from 'react';
import { User } from '../types/task';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: any }>;
  register: (email: string, password: string) => Promise<{ success: boolean; error?: any }>;
  logout: () => void;
  refetchUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

// Get backend URL from environment variable
const BACKEND_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);

  const refetchUser = async () => {
    const token = localStorage.getItem('better-auth.session_token');

    if (token) {
      try {
        const response = await fetch(`${BACKEND_URL}/api/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data?.user) {
            setUser(data.user);
            setIsAuthenticated(true);
          }
        } else {
          throw new Error('Failed to fetch user');
        }
      } catch (err) {
        console.error('Failed to fetch user:', err);
        setUser(null);
        setIsAuthenticated(false);
      }
    } else {
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  useEffect(() => {
    refetchUser();
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    setError(null);
    try {
      const response = await fetch(`${BACKEND_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data?.token) {
          localStorage.setItem('better-auth.session_token', data.token);
          await refetchUser();
          return { success: true };
        } else {
          throw new Error('No token returned from server');
        }
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }
    } catch (err) {
      setError('Login failed. Please check your credentials.');
      console.error('Login error:', err);
      return { success: false, error: err };
    }
  };

  const register = async (email: string, password: string) => {
    setError(null);
    try {
      const response = await fetch(`${BACKEND_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data?.token) {
          localStorage.setItem('better-auth.session_token', data.token);
          await refetchUser();
          return { success: true };
        } else {
          throw new Error('No token returned from server');
        }
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }
    } catch (err) {
      setError('Registration failed. Email might already be in use.');
      console.error('Registration error:', err);
      return { success: false, error: err };
    }
  };

  const logout = async () => {
    localStorage.removeItem('better-auth.session_token');
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    refetchUser
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
