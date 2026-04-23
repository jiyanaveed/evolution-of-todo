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
  refetchUser: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

// Get backend URL from environment variable
const BACKEND_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

function formatApiDetail(detail: unknown): string {
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((e: { msg?: string; loc?: unknown } | string) =>
        typeof e === 'string' ? e : e?.msg ?? JSON.stringify(e),
      )
      .join(' ');
  }
  if (detail && typeof detail === 'object' && 'msg' in (detail as object)) {
    return String((detail as { msg: string }).msg);
  }
  return detail != null ? String(detail) : '';
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);

  /** Resolves to true if the current token yields a valid session from /api/auth/me */
  const refetchUser = async (): Promise<boolean> => {
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
            const u = data.user;
            setUser({
              id: String(u.id),
              email: u.email,
              created_at: (u.createdAt as string) ?? (u.created_at as string) ?? '',
            });
            setIsAuthenticated(true);
            return true;
          }
          setUser(null);
          setIsAuthenticated(false);
          return false;
        }
        setUser(null);
        setIsAuthenticated(false);
        return false;
      } catch (err) {
        console.error('Failed to fetch user:', err);
        setUser(null);
        setIsAuthenticated(false);
        return false;
      }
    } else {
      setUser(null);
      setIsAuthenticated(false);
    }
    return false;
  };

  useEffect(() => {
    void (async () => {
      await refetchUser();
      setLoading(false);
    })();
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
          const sessionOk = await refetchUser();
          if (!sessionOk) {
            localStorage.removeItem('better-auth.session_token');
            const msg =
              'Signed in, but the server could not verify your session. Check NEXT_PUBLIC_API_BASE_URL and that the API is running.';
            setError(msg);
            return { success: false, error: new Error(msg) };
          }
          return { success: true };
        } else {
          throw new Error('No token returned from server');
        }
      } else {
        let msg = 'Login failed';
        try {
          const errorData = await response.json();
          msg = formatApiDetail(errorData.detail) || msg;
        } catch {
          msg = response.statusText || msg;
        }
        throw new Error(msg);
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Login failed. Please check your credentials.';
      setError(message);
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
          const sessionOk = await refetchUser();
          if (!sessionOk) {
            localStorage.removeItem('better-auth.session_token');
            const msg =
              'Account created, but the server could not verify your session. Check NEXT_PUBLIC_API_BASE_URL and that the API is running.';
            setError(msg);
            return { success: false, error: new Error(msg) };
          }
          return { success: true };
        } else {
          throw new Error('No token returned from server');
        }
      } else {
        let msg = 'Registration failed';
        try {
          const errorData = await response.json();
          msg = formatApiDetail(errorData.detail) || msg;
        } catch {
          msg = response.statusText || msg;
        }
        throw new Error(msg);
      }
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : 'Registration failed. Email might already be in use.';
      setError(message);
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
