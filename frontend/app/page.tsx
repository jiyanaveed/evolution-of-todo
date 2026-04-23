'use client';

import React, { useState, useEffect, useCallback, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Header from '../components/Header';
import AIChatBox from '../components/AIChatBoxBase';
import ErrorBoundary from '../components/ErrorBoundary';
import useTasks from '../hooks/useTasks';
import { useAuth } from '../contexts/AuthContext';
import Link from 'next/link';
import ThemeSelector from '../components/ThemeSelector';
import DashboardTaskSection from '../components/DashboardTaskSection';
import {
  THEME_STORAGE_KEY,
  type DashboardThemeId,
  normalizeStoredTheme,
} from '../lib/dashboard-themes';

function isThemeId(s: string | null): s is DashboardThemeId {
  if (!s) return false;
  return s === 'clean' || s === 'kanban' || s === 'adventure';
}

function HomeDashboard() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const searchParams = useSearchParams();
  const router = useRouter();

  const [theme, setTheme] = useState<DashboardThemeId>('clean');
  const [showWelcome, setShowWelcome] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const {
    tasks,
    loading,
    error,
    fetchTasks,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  } = useTasks(user?.id);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    try {
      const raw = localStorage.getItem(THEME_STORAGE_KEY);
      setTheme(normalizeStoredTheme(raw));
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    const t = searchParams.get('theme');
    if (isThemeId(t)) {
      setTheme(t);
      try {
        localStorage.setItem(THEME_STORAGE_KEY, t);
      } catch {
        /* ignore */
      }
      router.replace('/', { scroll: false });
    }
  }, [searchParams, router]);

  useEffect(() => {
    if (searchParams.get('welcome') === '1') {
      setShowWelcome(true);
      const id = setTimeout(() => {
        setShowWelcome(false);
        router.replace('/', { scroll: false });
      }, 6000);
      return () => clearTimeout(id);
    }
  }, [searchParams, router]);

  useEffect(() => {
    setConversationId(null);
  }, []);

  const handleThemeChange = useCallback((id: DashboardThemeId) => {
    setTheme(id);
    try {
      localStorage.setItem(THEME_STORAGE_KEY, id);
    } catch {
      /* ignore */
    }
  }, []);

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
    void fetchTasks().catch((err) => {
      console.error('Failed to refresh tasks after AI mutation', err);
    });
  };

  const pageShell = 'min-h-screen bg-gray-50';

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
            <h1 className="text-3xl font-bold text-gray-800 mb-4">Momentum AI</h1>
            <p className="text-gray-600 mb-8">Sign in to manage your tasks and AI assistant</p>
            <Link
              href="/login"
              className="inline-block px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Sign in
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={pageShell}>
      <Header />
      {showWelcome && (
        <div className="bg-emerald-50 border-b border-emerald-200 text-emerald-900 px-4 py-3 text-center text-sm sm:text-base">
          <strong>Account created.</strong> You&apos;re signed in — welcome to Momentum AI.
        </div>
      )}
      <main className="container mx-auto p-3 sm:p-4 max-w-6xl">
        <div className="mb-4">
          <p className="text-sm text-gray-600 max-w-2xl">
            Pick how tasks are shown.{' '}
            <span className="text-gray-500">Adventure uses quest cards here; the full path map is on a separate page.</span>
          </p>
          <div className="mt-3">
            <ThemeSelector value={theme} onChange={handleThemeChange} />
          </div>
        </div>

        <div className="mt-4 grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8 items-start w-full min-w-0">
          <div className="min-w-0">
            <h2 className="text-lg sm:text-xl font-bold text-gray-800 mb-2">AI assistant</h2>
            <ErrorBoundary>
              <AIChatBox
                conversationId={conversationId || ''}
                onMutationSuccess={handleMutationSuccess}
                compact
              />
            </ErrorBoundary>
          </div>

          <div className="min-w-0 w-full max-w-full">
            <h2 className="text-lg sm:text-xl font-bold text-gray-800 mb-2">Tasks</h2>
            <ErrorBoundary>
              <DashboardTaskSection
                theme={theme}
                tasks={tasks}
                loading={loading}
                error={error}
                onUpdateTask={handleUpdateTask}
                onDeleteTask={handleDeleteTask}
                onToggleTask={handleToggleTask}
              />
            </ErrorBoundary>
          </div>
        </div>
      </main>
    </div>
  );
}

export default function HomePage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto" />
            <p className="mt-4 text-gray-600">Loading...</p>
          </div>
        </div>
      }
    >
      <HomeDashboard />
    </Suspense>
  );
}
