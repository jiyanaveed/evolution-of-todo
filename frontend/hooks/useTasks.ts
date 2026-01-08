import { useState, useEffect } from 'react';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '../types/task';
import taskApi from '../lib/task-api';

const useTasks = (userId: string | null | undefined) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [operationLoading, setOperationLoading] = useState<{[key: string]: boolean}>({});

  // Fetch user's tasks
  const fetchTasks = async () => {
    if (!userId) {
      setTasks([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const tasksData = await taskApi.getTasks(userId);
      setTasks(tasksData);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Create a new task
  const createTask = async (taskData: CreateTaskRequest) => {
    if (!userId) return;

    const operationId = `create-${Date.now()}`;
    setOperationLoading(prev => ({ ...prev, [operationId]: true }));

    try {
      setError(null);
      const newTask = await taskApi.createTask(userId, taskData);
      setTasks(prev => [...prev, newTask]);
    } catch (err) {
      setError('Failed to create task');
      console.error('Error creating task:', err);
    } finally {
      setOperationLoading(prev => {
        const newLoading = { ...prev };
        delete newLoading[operationId];
        return newLoading;
      });
    }
  };

  // Update a task
  const updateTask = async (id: number, taskData: UpdateTaskRequest) => {
    if (!userId) return;

    const operationId = `update-${id}`;
    setOperationLoading(prev => ({ ...prev, [operationId]: true }));

    try {
      setError(null);
      const updatedTask = await taskApi.updateTask(userId, id, taskData);
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    } finally {
      setOperationLoading(prev => {
        const newLoading = { ...prev };
        delete newLoading[operationId];
        return newLoading;
      });
    }
  };

  // Delete a task
  const deleteTask = async (id: number) => {
    if (!userId) return;

    const operationId = `delete-${id}`;
    setOperationLoading(prev => ({ ...prev, [operationId]: true }));

    try {
      setError(null);
      await taskApi.deleteTask(userId, id);
      setTasks(prev => prev.filter(task => task.id !== id));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    } finally {
      setOperationLoading(prev => {
        const newLoading = { ...prev };
        delete newLoading[operationId];
        return newLoading;
      });
    }
  };

  // Toggle task completion
  const toggleTaskCompletion = async (id: number) => {
    if (!userId) return;

    const operationId = `toggle-${id}`;
    setOperationLoading(prev => ({ ...prev, [operationId]: true }));

    try {
      setError(null);
      const updatedTask = await taskApi.toggleTaskCompletion(userId, id);
      setTasks(prev => prev.map(task =>
        task.id === id ? updatedTask : task
      ));
    } catch (err) {
      setError('Failed to toggle task completion');
      console.error('Error toggling task completion:', err);
    } finally {
      setOperationLoading(prev => {
        const newLoading = { ...prev };
        delete newLoading[operationId];
        return newLoading;
      });
    }
  };

  // Initialize tasks on mount and when userId changes
  useEffect(() => {
    fetchTasks();
  }, [userId]);

  // Determine if any operation is loading
  const isAnyOperationLoading = Object.values(operationLoading).some(loading => loading);

  return {
    tasks,
    loading,
    error,
    isAnyOperationLoading,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
};

export default useTasks;