'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import QuestMap from '../../components/QuestMap';
import QuestTaskList from '../../components/QuestTaskList';
import AINarrator from '../../components/AINarrator';
import { Task } from '../../types/task';

type QuestTask = Task & { xp?: number; status?: string; description?: string };
import { useAuth } from '../../contexts/AuthContext';
import Header from '../../components/Header';
import useTasks from '../../hooks/useTasks';

export default function QuestMapPage() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<QuestTask[]>([]);
  const [narratorMessage, setNarratorMessage] = useState<string>(
    'Welcome, adventurer! Your journey begins here...'
  );
  const [heroPosition, setHeroPosition] = useState<number>(0);

  const {
    tasks: fetchedTasks,
    loading: tasksLoading,
    error: tasksError,
    toggleTaskCompletion,
  } = useTasks(user?.id);

  useEffect(() => {
    if (fetchedTasks && !tasksLoading) {
      const extendedTasks: QuestTask[] = fetchedTasks.map((task) => ({
        ...task,
        xp: 50 + (task.title.length % 50),
        status: task.completed ? 'completed' : 'pending',
        description: task.title,
      }));
      setTasks(extendedTasks);
    }
  }, [fetchedTasks, tasksLoading]);

  useEffect(() => {
    const completedCount = tasks.filter((t) => t.completed).length;
    setHeroPosition(completedCount);
    if (completedCount === 0) {
      setNarratorMessage(
        "Welcome, adventurer! Your journey begins here. Complete quests to move along the path."
      );
    } else if (completedCount === 1) {
      setNarratorMessage("Great start! You've completed your first quest. Keep going!");
    } else {
      setNarratorMessage("You're making real progress. Continue your adventure!");
    }
  }, [tasks]);

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-400 mx-auto"></div>
          <p className="mt-4 text-yellow-200">Loading your adventure...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center py-12 px-4">
        <div className="max-w-md w-full space-y-8 text-center">
          <h1 className="text-4xl font-bold text-yellow-300 mb-4">Quest map</h1>
          <p className="text-lg text-yellow-100 mb-8">Sign in to see your full quest path.</p>
          <Link
            href="/login"
            className="inline-block px-6 py-3 rounded-md text-yellow-900 bg-yellow-400 hover:bg-yellow-300 font-medium"
          >
            Sign in
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-indigo-900 text-white overflow-x-hidden">
      <Header />
      <AINarrator message={narratorMessage} />

      <main className="container mx-auto p-4 max-w-6xl relative z-10 w-full min-w-0">
        <div className="mb-2">
          <Link
            href="/"
            className="text-sm text-amber-200 hover:text-white underline decoration-amber-500/50"
          >
            ← Back to dashboard
          </Link>
        </div>

        <div className="text-center mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold text-yellow-300 mb-2">Quest map</h1>
          <p className="text-base sm:text-lg text-yellow-100 px-2">
            Full-screen path. Same tasks as your main dashboard.
          </p>
        </div>

        {tasksError && (
          <div className="mb-4 rounded-lg bg-red-900/40 border border-red-500/50 p-3 text-sm text-red-100">
            {tasksError}
          </div>
        )}

        <div className="mb-8 w-full min-w-0">
          {tasks.length > 0 ? (
            <div className="w-full min-h-[12rem] sm:min-h-[16rem]">
              <QuestMap tasks={tasks} heroPosition={heroPosition} />
            </div>
          ) : (
            <div className="rounded-xl border-2 border-dashed border-amber-600/50 py-12 text-amber-200/80 text-center text-sm">
              Add tasks on the main dashboard to build your path.
            </div>
          )}
        </div>

        <div className="bg-black/30 backdrop-blur-sm rounded-xl p-4 sm:p-6 border-2 border-yellow-600/60 w-full min-w-0">
          <h2 className="text-xl sm:text-2xl font-bold text-yellow-300 mb-4 flex items-center">
            <span className="mr-2">⚔️</span> Your quests
          </h2>
          {tasksLoading ? (
            <p className="text-amber-100/80">Loading quests…</p>
          ) : (
            <div className="w-full min-w-0">
              <QuestTaskList
                tasks={tasks}
                onSelectTask={() => {}}
                onTaskToggle={(taskId) => toggleTaskCompletion(taskId)}
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
