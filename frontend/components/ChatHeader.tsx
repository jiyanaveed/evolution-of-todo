/**
 * Chat Header Component
 * Shows app name, user info, and logout button
 */

'use client';

import React from 'react';
import { useAuth } from '../contexts/AuthContext';

export default function ChatHeader() {
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="bg-white border-b border-gray-200 py-4 px-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-indigo-600 rounded-lg p-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">TaskFlow AI</h1>
            <p className="text-xs text-gray-500">AI-Powered Task Management</p>
          </div>
        </div>

        {isAuthenticated && user && (
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="bg-gray-200 rounded-full p-2">
                <span className="text-sm font-medium text-gray-700">
                  {user.email.charAt(0).toUpperCase()}
                </span>
              </div>
              <span className="text-sm font-medium text-gray-700 hidden md:inline">
                {user.email.split('@')[0]}
              </span>
            </div>
            <button
              onClick={handleLogout}
              className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
}