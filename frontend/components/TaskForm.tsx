import React, { useState } from 'react';
import { CreateTaskRequest } from '../types/task';

interface TaskFormProps {
  onCreateTask: (taskTitle: string) => void;
  isLoading?: boolean;
}

const TaskForm = ({ onCreateTask, isLoading = false }: TaskFormProps) => {
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Task title cannot be empty');
      return;
    }

    setError('');
    onCreateTask(title.trim());
    setTitle('');
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="flex gap-2">
        <input
          type="text"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (error) setError(''); // Clear error when user starts typing
          }}
          placeholder="Enter a new task..."
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !title.trim()}
          className={`px-4 py-3 rounded-lg font-medium ${
            isLoading || !title.trim()
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-indigo-600 text-white hover:bg-indigo-700'
          }`}
        >
          {isLoading ? 'Adding...' : 'Add Task'}
        </button>
      </div>
      {error && <p className="mt-2 text-red-500 text-sm">{error}</p>}
    </form>
  );
};

export default TaskForm;