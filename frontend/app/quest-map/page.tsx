'use client';

import React, { useState, useEffect } from 'react';
import QuestMap from '../../components/QuestMap';
import QuestTaskList from '../../components/QuestTaskList';
import AINarrator from '../../components/AINarrator';
import { Task } from '../../types/task';
import { useAuth } from '../../contexts/AuthContext';
import Header from '../../components/Header';
import useTasks from '../../hooks/useTasks';

export default function QuestMapPage() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [narratorMessage, setNarratorMessage] = useState<string>('Welcome, adventurer! Your journey begins here...');
  const [heroPosition, setHeroPosition] = useState<number>(0);

  // Use the existing useTasks hook to get real tasks
  const {
    tasks: fetchedTasks,
    loading: tasksLoading,
    error: tasksError,
    isAnyOperationLoading,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  } = useTasks(user?.id);

  // Update local tasks state when fetched tasks change
  useEffect(() => {
    if (fetchedTasks && !tasksLoading) {
      // Transform real tasks to extended task format with RPG properties
      const extendedTasks = fetchedTasks.map(task => ({
        ...task,
        xp: 50 + (task.title.length % 50), // Dynamic XP based on task
        status: task.completed ? 'completed' : 'pending',
        description: task.title // Using title as description for now
      }));

      setTasks(extendedTasks);
    }
  }, [fetchedTasks, tasksLoading]);

  // Update hero position based on completed tasks
  useEffect(() => {
    const completedCount = tasks.filter(task => task.completed).length;
    setHeroPosition(completedCount);
    
    // Update narrator message based on progress
    if (completedCount === 0) {
      setNarratorMessage('Welcome, adventurer! Your journey begins here. Complete quests to progress through the story.');
    } else if (completedCount === 1) {
      setNarratorMessage('Great start! You\'ve completed your first quest. Keep going!');
    } else if (completedCount >= 2) {
      setNarratorMessage('Amazing progress! You\'re becoming a true hero. Continue your adventure!');
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
          <div>
            <h1 className="text-4xl font-bold text-yellow-300 mb-4">Quest Adventure</h1>
            <p className="text-xl text-yellow-100 mb-8">Embark on an epic journey to complete your tasks!</p>
            <button 
              className="px-6 py-3 border border-transparent text-base font-medium rounded-md text-yellow-900 bg-yellow-400 hover:bg-yellow-300"
              onClick={() => window.location.href = '/login'}
            >
              Begin Your Quest
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 via-blue-900 to-indigo-900 text-white overflow-hidden">
      <Header />

      {/* AI Narrator floating box */}
      <AINarrator message={narratorMessage} />

      <main className="container mx-auto p-4 max-w-6xl relative z-10">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-yellow-300 mb-2">Quest Adventure Map</h1>
          <p className="text-lg text-yellow-100">Complete quests to progress through your story</p>
        </div>

        {/* Quest Map */}
        <div className="mb-8">
          <QuestMap tasks={tasks} heroPosition={heroPosition} />
        </div>

        {/* Quest List */}
        <div className="bg-black bg-opacity-30 backdrop-blur-sm rounded-xl p-6 border-2 border-yellow-600">
          <h2 className="text-2xl font-bold text-yellow-300 mb-4 flex items-center">
            <span className="mr-2">⚔️</span> Your Quests
          </h2>
          <QuestTaskList
            tasks={tasks}
            onSelectTask={setSelectedTask}
            onTaskToggle={(taskId) => {
              toggleTaskCompletion(taskId);
            }}
          />
        </div>
      </main>
    </div>
  );
}

// Extend Task interface with RPG-specific properties
interface ExtendedTask extends Task {
  xp?: number;
  status?: 'pending' | 'completed' | 'locked';
  description?: string;
}