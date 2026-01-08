import React, { useEffect, useState, forwardRef, useImperativeHandle } from 'react';
import axios from 'axios';

interface Task {
  id: number;
  title: string;
  completed: boolean;
}

export interface TaskSidebarRef {
  refresh: () => void;
}

/**
 * TaskSidebar.tsx - A read-only visualization of the user's task state.
 * RULE: [Stateless] Refetches when signaled by ChatBox mutation confirm.
 * RULE: [Completion Constraint] Completed tasks are immutable (no undo).
 * RULE: [Ownership] JWT context handles filtering.
 */
const TaskSidebar = forwardRef<TaskSidebarRef>((_, ref) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [syncing, setSyncing] = useState(false);

  const fetchTasks = async () => {
    setSyncing(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get<Task[]>('http://localhost:8000/tasks', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTasks(response.data);
    } finally {
      setSyncing(false);
    }
  };

  useImperativeHandle(ref, () => ({ refresh: fetchTasks }));

  useEffect(() => { fetchTasks(); }, []);

  return (
    <div className="w-[300px] h-[550px] border border-gray-200 rounded-xl bg-gray-50 shadow-sm flex flex-col">
      <div className="p-4 border-b bg-white rounded-t-xl flex justify-between items-center">
        <h2 className="text-sm font-bold text-gray-700 uppercase tracking-widest">Active State</h2>
        {syncing && <div className="animate-pulse w-2 h-2 bg-indigo-500 rounded-full" />}
      </div>

      <div className="p-4 overflow-y-auto space-y-3 flex-1">
        {tasks.length === 0 && !syncing && <p className="text-xs text-center text-gray-400 italic py-10">Empty set. Add tasks via chat.</p>}
        {tasks.map(t => (
          <div key={t.id} className={`p-3 rounded-lg border flex flex-col gap-1 transition-all ${t.completed ? 'bg-green-50/50 border-green-100' : 'bg-white border-gray-100'}`}>
            <div className="flex justify-between items-start">
               <span className="text-[9px] font-mono text-gray-400">#00{t.id}</span>
               {t.completed && <span className="text-[10px] font-black text-green-600 uppercase">Static</span>}
            </div>
            {/* RULE: [Completion Constraint] Visual strike-through only; no interactive revert path. */}
            <p className={`text-sm ${t.completed ? 'line-through text-gray-400 font-normal italic' : 'text-gray-700 font-semibold'}`}>
              {t.title}
            </p>
          </div>
        ))}
      </div>

      <div className="p-3 border-t bg-white rounded-b-xl">
         <p className="text-[9px] text-gray-400 text-center uppercase tracking-tighter">AI-First Deterministic Mirror</p>
      </div>
    </div>
  );
});

TaskSidebar.displayName = 'TaskSidebar';
export default TaskSidebar;
