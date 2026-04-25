import React, { useState } from 'react';
import { Task, UpdateTaskRequest } from '../types/task';
export type TaskItemVariant = 'default' | 'kanban';

interface TaskItemProps {
  task: Task;
  onUpdateTask: (id: number, taskData: UpdateTaskRequest) => void;
  onDeleteTask: (id: number) => void;
  onToggleTask: (id: number) => void;
  isLoading?: boolean;
  variant?: TaskItemVariant;
}

const TaskItem = ({ task, onUpdateTask, onDeleteTask, onToggleTask, isLoading = false, variant = 'default' }: TaskItemProps) => {
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

  const isKanban = variant === 'kanban';
  const itemShell = isKanban
    ? 'mb-0 w-full min-w-0 max-w-full rounded-xl border p-3.5 transition duration-200 ease-out hover:-translate-y-0.5 sm:p-4 ' +
      (task.completed
        ? 'border-emerald-500/40 bg-slate-900/60 shadow-[0_0_0_1px_rgba(52,211,153,0.15),0_0_20px_rgba(52,211,153,0.12)] hover:shadow-[0_0_0_1px_rgba(52,211,153,0.28),0_0_24px_rgba(52,211,153,0.18)]'
        : 'border-cyan-500/35 bg-slate-900/80 shadow-[0_0_0_1px_rgba(34,211,238,0.12),0_0_18px_rgba(34,211,238,0.1)] hover:shadow-[0_0_0_1px_rgba(34,211,238,0.35),0_0_22px_rgba(34,211,238,0.16)]')
    : 'p-3 border rounded-lg mb-2 ' + (task.completed ? 'bg-green-50' : 'bg-white') + ' min-w-0';

  const defaultActions = () => (
    <>
      {isEditing ? (
        <>
          <button
            type="button"
            onClick={handleSave}
            className={
              isKanban
                ? 'rounded-lg p-2 text-sm text-emerald-300 transition hover:bg-emerald-500/10 hover:shadow-[0_0_12px_rgba(52,211,153,0.35)]'
                : 'text-green-600 hover:text-green-800 p-1'
            }
            disabled={isLoading}
          >
            ✓
          </button>
          <button
            type="button"
            onClick={handleCancel}
            className={
              isKanban
                ? 'rounded-lg p-2 text-sm text-slate-400 transition hover:bg-slate-800/80 hover:shadow-[0_0_10px_rgba(148,163,184,0.2)]'
                : 'text-red-600 hover:text-red-800 p-1'
            }
            disabled={isLoading}
          >
            ✕
          </button>
        </>
      ) : (
        <>
          <button
            type="button"
            onClick={handleEdit}
            className={
              isKanban
                ? 'rounded-lg p-2 text-slate-400 transition hover:bg-violet-500/10 hover:text-cyan-200 hover:shadow-[0_0_12px_rgba(34,211,238,0.3)]'
                : 'text-blue-600 hover:text-blue-800 p-1'
            }
            disabled={isLoading}
            title="Edit"
            aria-label="Edit task"
          >
            ✏️
          </button>
          {deleteConfirm ? (
            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={handleDelete}
                className={
                  isKanban
                    ? 'rounded-lg px-2.5 py-1.5 text-xs font-medium text-rose-400 transition hover:bg-rose-500/15 hover:shadow-[0_0_10px_rgba(244,63,94,0.3)]'
                    : 'text-red-600 hover:text-red-800 p-1 text-xs'
                }
                disabled={isLoading}
              >
                Yes
              </button>
              <button
                type="button"
                onClick={() => setDeleteConfirm(false)}
                className={
                  isKanban
                    ? 'rounded-lg px-2.5 py-1.5 text-xs font-medium text-slate-400 transition hover:bg-slate-800/80 hover:shadow-[0_0_8px_rgba(148,163,184,0.2)]'
                    : 'text-gray-600 hover:text-gray-800 p-1 text-xs'
                }
                disabled={isLoading}
              >
                No
              </button>
            </div>
          ) : (
            <button
              type="button"
              onClick={handleDelete}
              className={
                isKanban
                  ? 'rounded-lg p-2 text-slate-400 transition hover:bg-rose-500/10 hover:text-rose-300 hover:shadow-[0_0_12px_rgba(244,63,94,0.25)]'
                  : 'text-red-600 hover:text-red-800 p-1'
              }
              disabled={isLoading}
              title="Delete"
              aria-label="Delete task"
            >
              🗑️
            </button>
          )}
        </>
      )}
    </>
  );

  if (isKanban) {
    const rowGrid: React.CSSProperties = {
      display: 'grid',
      boxSizing: 'border-box',
      width: '100%',
      minWidth: 0,
      maxWidth: '100%',
      // Inline so production never drops arbitrary Tailwind grid cols; 1fr middle must be minmax(0,1fr)
      gridTemplateColumns: 'auto minmax(0, 1fr) auto',
      columnGap: '0.7rem',
      alignItems: 'start',
    };
    return (
      <div
        className={`${itemShell} min-w-0`}
        style={{ width: '100%', minWidth: 0, boxSizing: 'border-box' }}
      >
        <div style={rowGrid}>
          <div className="flex items-start gap-2.5">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggleTask(task.id)}
              disabled={isLoading || task.completed}
              className="mt-0.5 h-[18px] w-[18px] shrink-0 cursor-pointer rounded border-cyan-500/50 bg-slate-800 text-cyan-400 accent-cyan-500 focus:ring-2 focus:ring-cyan-500/40"
            />
            {!isEditing &&
              (!task.completed ? (
                <span
                  className="mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.9)]"
                  aria-hidden
                />
              ) : (
                <span
                  className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-emerald-400/50 bg-emerald-500/20 text-sm font-bold text-emerald-300 shadow-[0_0_10px_rgba(52,211,153,0.45)]"
                  aria-hidden
                >
                  ✓
                </span>
              ))}
          </div>
          <div
            className="kanban-task-mid"
            style={{ minWidth: 0, maxWidth: '100%' }}
          >
            {isEditing ? (
              <input
                type="text"
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
                onKeyDown={handleKeyDown}
                onBlur={handleSave}
                className="box-border w-full min-w-0 max-w-full rounded-lg border border-cyan-500/40 bg-slate-800/80 px-2.5 py-1.5 text-base font-medium text-slate-100 placeholder-slate-500 focus:border-cyan-400/70 focus:outline-none focus:ring-2 focus:ring-cyan-500/30"
                autoFocus
              />
            ) : (
              <div
                className="min-w-0 w-full max-w-full"
                style={{ minWidth: 0 }}
              >
                <p
                  className={`text-left text-base font-semibold leading-snug ${
                    task.completed ? 'text-slate-500' : 'text-slate-100'
                  }`}
                  style={{
                    margin: 0,
                    minWidth: 0,
                    maxWidth: '100%',
                    width: '100%',
                    wordBreak: 'normal',
                    overflowWrap: 'break-word',
                    whiteSpace: 'normal',
                  }}
                  onDoubleClick={handleEdit}
                >
                  {task.title}
                </p>
                <p className="mt-1 text-left text-xs font-medium text-slate-500">
                  {task.completed ? 'Completed' : 'To do'}
                </p>
              </div>
            )}
          </div>
          <div className="flex shrink-0 items-start gap-0.5 pt-0.5 sm:gap-1">
            {defaultActions()}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex items-center justify-between gap-2 ${itemShell}`}>
      <div className="flex items-center flex-1 min-w-0">
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
            className={`flex-1 min-w-0 break-words ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}
            onDoubleClick={handleEdit}
          >
            {task.title}
          </span>
        )}
      </div>
      <div className="flex gap-2 shrink-0">
        {defaultActions()}
      </div>
    </div>
  );
};

export default TaskItem;