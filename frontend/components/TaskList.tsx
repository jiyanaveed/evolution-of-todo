import React from 'react';
import { Task } from '../types/task';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onUpdateTask: (id: number, title: string) => void;
  onDeleteTask: (id: number) => void;
  onToggleTask: (id: number) => void;
  isLoading?: boolean;
  error?: string | null;
}

const TaskList = ({ tasks, onUpdateTask, onDeleteTask, onToggleTask, isLoading = false, error = null }: TaskListProps) => {
  if (isLoading) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
        <p className="text-red-600">Error: {error}</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No tasks yet. Add your first task above!</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Your Tasks</h2>
      <div>
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onUpdateTask={(id, taskData) => onUpdateTask(id, taskData.title || task.title)}
            onDeleteTask={onDeleteTask}
            onToggleTask={onToggleTask}
            isLoading={isLoading}
          />
        ))}
      </div>
    </div>
  );
};

export default TaskList;