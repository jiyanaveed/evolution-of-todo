'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../contexts/AuthContext';
import { getPublicApiBaseUrl } from '../../lib/api-base';

function humanizeAuthError(message: string): string {
  const m = message.toLowerCase();
  if (m.includes('already') || m.includes('exists')) {
    return 'An account with this email already exists. Sign in instead, or use a different email.';
  }
  if (
    m.includes('incorrect') ||
    m.includes('invalid') ||
    m.includes('401') ||
    m.includes('unauthorized') ||
    m.includes('credentials')
  ) {
    return 'Email or password is incorrect. Please try again.';
  }
  if (m.includes('network') || m.includes('fetch')) {
    return 'Could not reach the server. Check that the API is running and NEXT_PUBLIC_API_BASE_URL is correct.';
  }
  return message;
}

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true);
  const { login, register, error, isAuthenticated } = useAuth();
  const router = useRouter();

  React.useEffect(() => {
    if (!isAuthenticated) return;
    const welcome = typeof window !== 'undefined' && sessionStorage.getItem('momentum_welcome');
    if (welcome) {
      sessionStorage.removeItem('momentum_welcome');
      router.replace('/?welcome=1');
      return;
    }
    router.push('/');
  }, [isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (isLogin) {
      const result = await login(email, password);
      if (!result.success) return;
      if (typeof window !== 'undefined') {
        sessionStorage.removeItem('momentum_welcome');
      }
      return;
    }

    const result = await register(email, password);
    if (result.success && typeof window !== 'undefined') {
      sessionStorage.setItem('momentum_welcome', '1');
    }
  };

  const displayError = error ? humanizeAuthError(error) : null;

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {isLogin ? 'Sign in to Momentum AI' : 'Create your account'}
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            {isLogin ? 'Welcome back' : 'Sign up to sync tasks and AI on any device'}
          </p>
          {process.env.NODE_ENV === 'development' && (
            <p className="mt-2 text-center text-xs text-gray-400 font-mono break-all" title="API base URL (dev only)">
              API base: {getPublicApiBaseUrl()}
            </p>
          )}
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {displayError && (
            <div className="bg-red-100 border border-red-400 text-red-800 px-4 py-3 rounded relative" role="alert">
              <span className="block sm:inline">{displayError}</span>
            </div>
          )}

          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email-address" className="sr-only">
                Email address
              </label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Email address"
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete={isLogin ? 'current-password' : 'new-password'}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Password"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {isLogin ? 'Sign in' : 'Create account'}
            </button>
          </div>
        </form>

        <div className="text-center mt-4">
          <button
            type="button"
            onClick={() => {
              setIsLogin(!isLogin);
              setEmail('');
              setPassword('');
            }}
            className="text-indigo-600 hover:text-indigo-500 text-sm"
          >
            {isLogin
              ? "Don't have an account? Sign up"
              : 'Already have an account? Sign in'}
          </button>
        </div>
      </div>
    </div>
  );
}
