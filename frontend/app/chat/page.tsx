'use client';

import React, { useState, useEffect } from 'react';
import ChatHeader from '../../components/ChatHeader';
import ChatContainer from '../../components/ChatContainer';
import { useAuth } from '../../contexts/AuthContext';
import Link from 'next/link';

export default function ChatPage() {
  const { user, isAuthenticated, loading: authLoading, logout } = useAuth();
  const [conversationId, setConversationId] = useState<string | null>(null);

  useEffect(() => {
    // Initialize with null to create new conversation on first message
    setConversationId(null);
  }, []);

  const handleMutationSuccess = () => {
    // This could trigger a refresh of related data if needed
    console.log('Mutation completed, refreshing data if needed...');
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8 text-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-4">TaskFlow AI</h1>
            <p className="text-gray-600 mb-8">Please log in to use the AI assistant</p>
            <Link
              href="/login"
              className="inline-block px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <ChatHeader />
      <main className="flex-1 container mx-auto p-4 max-w-4xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-800">TaskFlow AI Assistant</h1>
          <p className="text-gray-600 mt-1">Manage your tasks with natural language</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <ChatContainer
            conversationId={conversationId || ''}
            onMutationSuccess={handleMutationSuccess}
          />
        </div>
      </main>
    </div>
  );
}