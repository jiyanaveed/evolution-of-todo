'use client';

import React, { useMemo } from 'react';
import Link from 'next/link';
import { Task } from '../types/task';
import QuestCard from './QuestCard';

type Extended = Task & { xp?: number; status?: 'pending' | 'completed' | 'locked'; description?: string };

function toExtended(tasks: Task[]): Extended[] {
  return tasks.map((task) => ({
    ...task,
    xp: 50 + (task.title.length % 50),
    status: (task.completed ? 'completed' : 'pending') as 'pending' | 'completed' | 'locked',
    description: task.title,
  }));
}

type Props = {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  onToggleTask: (taskId: number) => void;
};

/**
 * Quest-style cards for the dashboard (no map). Full map lives on /quest-map.
 */
export default function DashboardQuestCardList({ tasks, loading, error, onToggleTask }: Props) {
  const extended = useMemo(() => toExtended(tasks), [tasks]);
  const pending = extended.filter((t) => t.status === 'pending');
  const done = extended.filter((t) => t.status === 'completed');

  if (loading) {
    return <p className="text-amber-100/80 text-sm py-4">Loading quests…</p>;
  }
  if (error) {
    return <p className="text-red-300 text-sm break-words">{error}</p>;
  }

  return (
    <div className="min-w-0">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-3">
        <h2 className="text-lg font-bold text-amber-200 flex items-center gap-2 min-w-0">
          <span className="shrink-0">⚔️</span>
          <span className="truncate">Your quests</span>
        </h2>
        <Link
          href="/quest-map"
          className="shrink-0 text-sm font-medium text-amber-300 hover:text-amber-100 underline decoration-amber-500/50 underline-offset-2"
        >
          Full quest map view →
        </Link>
      </div>
      <p className="text-xs text-amber-100/70 mb-4">
        Dashboard shows quest cards. Open the full page for the path map and larger layout.
      </p>

      {extended.length === 0 ? (
        <div className="rounded-lg border border-amber-800/50 bg-slate-900/50 px-3 py-8 text-center text-amber-200/80 text-sm">
          No quests yet — add a task in chat to begin.
        </div>
      ) : (
        <div className="space-y-6 min-w-0">
          {pending.length > 0 && (
            <section className="min-w-0">
              <h3 className="text-sm font-semibold text-amber-300/90 mb-2 flex items-center gap-2">
                <span>⏳</span> Active
              </h3>
              <div className="flex flex-col gap-3">
                {pending.map((task) => (
                  <div key={task.id} className="min-w-0 w-full max-w-full">
                    <QuestCard
                      task={task}
                      status="pending"
                      onSelect={() => {}}
                      onToggle={onToggleTask}
                      embed
                    />
                  </div>
                ))}
              </div>
            </section>
          )}
          {done.length > 0 && (
            <section className="min-w-0">
              <h3 className="text-sm font-semibold text-emerald-300/90 mb-2 flex items-center gap-2">
                <span>✅</span> Completed
              </h3>
              <div className="flex flex-col gap-3">
                {done.map((task) => (
                  <div key={task.id} className="min-w-0 w-full max-w-full">
                    <QuestCard
                      task={task}
                      status="completed"
                      onSelect={() => {}}
                      onToggle={onToggleTask}
                      embed
                    />
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>
      )}
    </div>
  );
}
