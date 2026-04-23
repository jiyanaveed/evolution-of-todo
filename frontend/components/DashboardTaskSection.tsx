'use client';

import React from 'react';
import { Task } from '../types/task';
import TaskList from './TaskList';
import TaskItem from './TaskItem';
import DashboardQuestCardList from './DashboardQuestCardList';
import type { DashboardThemeId } from '../lib/dashboard-themes';

type Props = {
  theme: DashboardThemeId;
  tasks: Task[];
  loading: boolean;
  error: string | null;
  onUpdateTask: (id: number, title: string) => void;
  onDeleteTask: (id: number) => void;
  onToggleTask: (id: number) => void;
};

function KanbanPanel({
  tasks,
  loading: loadingFlag,
  error,
  onUpdateTask,
  onDeleteTask,
  onToggleTask,
}: Omit<Props, 'theme'>) {
  if (loadingFlag) {
    return <p className="text-center text-cyan-200/50 py-6 text-sm">Loading tasks…</p>;
  }
  if (error) {
    return <p className="text-sm text-rose-400/90 p-2 break-words">Error: {error}</p>;
  }
  const open = tasks.filter((t) => !t.completed);
  const done = tasks.filter((t) => t.completed);
  return (
    <div className="kanban-board-cols">
      <div
        className="min-w-0 w-full max-w-full rounded-2xl border border-cyan-500/50 bg-slate-900/80 p-4 sm:p-5 shadow-[0_0_24px_rgba(34,211,238,0.12),inset_0_1px_0_0_rgba(34,211,238,0.12)]"
      >
        <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-200/90">
          To do <span className="font-mono text-cyan-300">({open.length})</span>
        </h3>
        <p className="mt-0.5 text-xs text-cyan-200/50">Not started or in progress</p>
        <div className="mt-4 flex w-full min-w-0 max-w-full flex-col gap-3.5">
          {open.length === 0 ? (
            <p className="rounded-xl border border-dashed border-cyan-500/30 bg-slate-950/50 py-8 text-center text-sm text-cyan-200/50">
              No tasks yet
            </p>
          ) : (
            open.map((task) => (
              <div key={task.id} className="w-full min-w-0 max-w-full">
                <TaskItem
                  task={task}
                  onUpdateTask={(id, d) => onUpdateTask(id, d.title || task.title)}
                  onDeleteTask={onDeleteTask}
                  onToggleTask={onToggleTask}
                  variant="kanban"
                />
              </div>
            ))
          )}
        </div>
      </div>
      <div
        className="min-w-0 w-full max-w-full rounded-2xl border border-emerald-500/45 bg-slate-900/80 p-4 sm:p-5 shadow-[0_0_24px_rgba(52,211,153,0.1),inset_0_1px_0_0_rgba(52,211,153,0.1)]"
      >
        <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-200/90">
          Done <span className="font-mono text-emerald-300">({done.length})</span>
        </h3>
        <p className="mt-0.5 text-xs text-emerald-200/50">Completed work</p>
        <div className="mt-4 flex w-full min-w-0 max-w-full flex-col gap-3.5">
          {done.length === 0 ? (
            <p className="rounded-xl border border-dashed border-emerald-500/30 bg-slate-950/50 py-8 text-center text-sm text-emerald-200/50">
              All caught up 🎉
            </p>
          ) : (
            done.map((task) => (
              <div key={task.id} className="w-full min-w-0 max-w-full">
                <TaskItem
                  task={task}
                  onUpdateTask={(id, d) => onUpdateTask(id, d.title || task.title)}
                  onDeleteTask={onDeleteTask}
                  onToggleTask={onToggleTask}
                  variant="kanban"
                />
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default function DashboardTaskSection({
  theme,
  tasks,
  loading,
  error,
  onUpdateTask,
  onDeleteTask,
  onToggleTask,
}: Props) {
  if (theme === 'adventure') {
    return (
      <div className="rounded-xl border border-amber-700/40 bg-slate-900 p-3 sm:p-4 text-white shadow-lg min-w-0 max-w-full">
        <DashboardQuestCardList
          tasks={tasks}
          loading={loading}
          error={error}
          onToggleTask={onToggleTask}
        />
      </div>
    );
  }

  if (theme === 'kanban') {
    const openCount = tasks.filter((t) => !t.completed).length;
    const doneCount = tasks.filter((t) => t.completed).length;
    return (
      <div className="min-w-0 w-full max-w-full rounded-2xl border border-violet-500/25 bg-gradient-to-b from-slate-950 via-slate-950 to-black p-4 shadow-[0_0_32px_rgba(99,102,241,0.12),0_0_1px_rgba(139,92,246,0.35)] sm:p-6">
        <div className="mb-3 flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between sm:gap-4">
          <h2 className="text-sm font-semibold tracking-tight text-slate-100">Board</h2>
          <p className="text-xs font-medium text-slate-500">
            <span className="text-cyan-300">To do {openCount}</span>
            <span className="mx-2 text-violet-500/60">·</span>
            <span className="text-emerald-300">Done {doneCount}</span>
          </p>
        </div>
        <p className="mb-4 text-xs text-slate-500">Open on the left, completed on the right — same actions as list view.</p>
        <KanbanPanel
          tasks={tasks}
          loading={loading}
          error={error}
          onUpdateTask={onUpdateTask}
          onDeleteTask={onDeleteTask}
          onToggleTask={onToggleTask}
        />
      </div>
    );
  }

  // clean
  return (
    <div className="min-w-0 max-w-full rounded-lg border border-gray-100 bg-white p-1 shadow-sm sm:p-2">
      <h2 className="text-lg sm:text-xl font-bold text-gray-800 mb-2 sm:mb-3 px-1 sm:px-0">Your tasks</h2>
      <TaskList
        tasks={tasks}
        onUpdateTask={onUpdateTask}
        onDeleteTask={onDeleteTask}
        onToggleTask={onToggleTask}
        isLoading={loading}
        error={error}
        showOuterTitle={false}
      />
    </div>
  );
}
