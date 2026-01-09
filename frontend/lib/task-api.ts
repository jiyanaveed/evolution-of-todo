import { Task, CreateTaskRequest, UpdateTaskRequest } from '../types/task';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

// Create an API client for task operations
const taskApi = {
  /**
   * Get all tasks for a user
   */
  getTasks: async (userId: string): Promise<Task[]> => {
    const response = await fetch(`${BACKEND_URL}/api/${userId}/tasks`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}`);
    }
    
    return response.json();
  },

  /**
   * Create a new task for a user
   */
  createTask: async (userId: string, taskData: CreateTaskRequest): Promise<Task> => {
    const response = await fetch(`${BACKEND_URL}/api/${userId}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: taskData.title,
        description: taskData.description || null
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to create task: ${response.status} ${response.statusText}`);
    }

    return response.json();
  },

  /**
   * Update an existing task
   */
  updateTask: async (userId: string, taskId: number, taskData: UpdateTaskRequest): Promise<Task> => {
    const response = await fetch(`${BACKEND_URL}/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: taskData.title,
        completed: taskData.completed
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to update task: ${response.status} ${response.statusText}`);
    }

    return response.json();
  },

  /**
   * Delete a task
   */
  deleteTask: async (userId: string, taskId: number): Promise<void> => {
    const response = await fetch(`${BACKEND_URL}/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
    }
  },

  /**
   * Toggle task completion status
   */
  toggleTaskCompletion: async (userId: string, taskId: number): Promise<Task> => {
    const response = await fetch(`${BACKEND_URL}/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });

    if (!response.ok) {
      throw new Error(`Failed to toggle task completion: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }
};

export default taskApi;