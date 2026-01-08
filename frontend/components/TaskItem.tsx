import React, { useState } from 'react';
import { Task, UpdateTaskRequest } from '../types/task';

interface TaskItemProps {
  task: Task;
  onUpdateTask: (id: number, taskData: UpdateTaskRequest) => void;
  onDeleteTask: (id: number) => void;
  onToggleTask: (id: number) => void;
  isLoading?: boolean;
}

const TaskItem = ({ task, onUpdateTask, onDeleteTask, onToggleTask, isLoading = false }: TaskItemProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(task.title);
  const [deleteConfirm, setDeleteConfirm] = useState(false);

  const handleEdit = () => {
    setIsEditing(true);
    setEditValue(task.title);
  };

  const handleSave = () => {
  const trimmedValue = String(editValue).trim(); // force string
  if (trimmedValue && trimmedValue !== task.title) {
    onUpdateTask(task.id, { title: trimmedValue });
  }
  setIsEditing(false);
};


  const handleCancel = () => {
    setEditValue(task.title);
    setIsEditing(false);
  };

  const handleDelete = () => {
    if (deleteConfirm) {
      onDeleteTask(task.id);
      setDeleteConfirm(false);
    } else {
      setDeleteConfirm(true);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSave();
    } else if (e.key === 'Escape') {
      handleCancel();
    }
  };

  return (
    <div className={`flex items-center justify-between p-3 border rounded-lg mb-2 ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      <div className="flex items-center flex-1">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggleTask(task.id)}
          disabled={isLoading || task.completed}
          className="h-5 w-5 mr-3"
        />
        {isEditing ? (
          <input
            type="text"
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onKeyDown={handleKeyDown}
            onBlur={handleSave}
            className="flex-1 p-1 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500"
            autoFocus
          />
        ) : (
          <span
            className={`flex-1 ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}
            onDoubleClick={handleEdit}
          >
            {task.title}
          </span>
        )}
      </div>
      <div className="flex gap-2">
        {isEditing ? (
          <>
            <button
              onClick={handleSave}
              className="text-green-600 hover:text-green-800 p-1"
              disabled={isLoading}
            >
              ✓
            </button>
            <button
              onClick={handleCancel}
              className="text-red-600 hover:text-red-800 p-1"
              disabled={isLoading}
            >
              ✕
            </button>
          </>
        ) : (
          <>
            <button
              onClick={handleEdit}
              className="text-blue-600 hover:text-blue-800 p-1"
              disabled={isLoading}
            >
              ✏️
            </button>
            {deleteConfirm ? (
              <div className="flex gap-1">
                <button
                  onClick={handleDelete}
                  className="text-red-600 hover:text-red-800 p-1 text-xs"
                  disabled={isLoading}
                >
                  Yes
                </button>
                <button
                  onClick={() => setDeleteConfirm(false)}
                  className="text-gray-600 hover:text-gray-800 p-1 text-xs"
                  disabled={isLoading}
                >
                  No
                </button>
              </div>
            ) : (
              <button
                onClick={handleDelete}
                className="text-red-600 hover:text-red-800 p-1"
                disabled={isLoading}
              >
                🗑️
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default TaskItem;