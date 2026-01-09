'use client';

import React from 'react';
import Header from '../components/Header';
import TaskList from '../components/TaskList';
import AIChatBox from '../components/AIChatBoxBase';
import ErrorBoundary from '../components/ErrorBoundary';
import useTasks from '../hooks/useTasks';
import { useAuth } from '../contexts/AuthContext';
import Link from 'next/link';

import { useState, useEffect } from 'react';

export default function HomePage() {
  const { user, isAuthenticated, loading: authLoading, logout } = useAuth();

  const {
    tasks,
    loading,
    error,
    isAnyOperationLoading,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  } = useTasks(user?.id);

  const [conversationId, setConversationId] = useState<string | null>(null); // Start with null to create new conversation

  // Initialize conversation ID
  useEffect(() => {
    // Start with null - backend will create a new conversation on first message
    setConversationId(null);
  }, []);

  const handleCreateTask = async (title: string) => {
    await createTask({ title });
  };

  const handleUpdateTask = async (id: number, title: string) => {
    await updateTask(id, { title });
  };

  const handleDeleteTask = async (id: number) => {
    await deleteTask(id);
  };

  const handleToggleTask = async (id: number) => {
    await toggleTaskCompletion(id);
  };

  const handleMutationSuccess = () => {
    // Re-fetch tasks handled by the hook's internal logic or manual trigger
    // Since useTasks has auto-refresh, we just need to ensure the state updates
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
            <h1 className="text-3xl font-bold text-gray-800 mb-4">Task Manager</h1>
            <p className="text-gray-600 mb-8">Please log in to manage your tasks</p>
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
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto p-4 max-w-6xl">
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800">AI Task Assistant</h2>
              <Link
                href="/quest-map"
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-sm"
              >
                🗺️ Adventure Mode
              </Link>
            </div>
            <ErrorBoundary>
              <AIChatBox conversationId={conversationId || ''} onMutationSuccess={handleMutationSuccess} />
            </ErrorBoundary>
          </div>

          <div className="lg:col-span-1">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Your Tasks</h2>
            <ErrorBoundary>
              <TaskList
                tasks={tasks}
                onUpdateTask={handleUpdateTask}
                onDeleteTask={handleDeleteTask}
                onToggleTask={handleToggleTask}
                isLoading={loading}
                error={error}
              />
            </ErrorBoundary>
          </div>
        </div>
      </main>
    </div>
  );
}// Deployment trigger Sat Jan 10 04:19:54 +08 2026
