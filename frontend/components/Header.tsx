'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';

const Header = () => {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header className="bg-indigo-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold">Evolution of Todo</Link>
        <nav>
          {isAuthenticated ? (
            <div className="flex items-center space-x-4">
              <span className="text-sm">Welcome, {user?.email}</span>
              <button
                onClick={logout}
                className="text-sm bg-white text-indigo-600 px-3 py-1 rounded hover:bg-gray-100"
              >
                Logout
              </button>
            </div>
          ) : (
            <Link
              href="/login"
              className="text-sm bg-white text-indigo-600 px-3 py-1 rounded hover:bg-gray-100"
            >
              Login
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;