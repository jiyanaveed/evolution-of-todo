import React from 'react';
import { Task } from '../../types/task';
import QuestCard from './QuestCard';

interface QuestTaskListProps {
  tasks: Array<Task & { xp?: number; status?: string; description?: string }>;
  onSelectTask: (task: Task) => void;
  onTaskToggle: (taskId: number) => void;
}

const QuestTaskList: React.FC<QuestTaskListProps> = ({ tasks, onSelectTask, onTaskToggle }) => {
  const pendingTasks = tasks.filter(task => task.status !== 'locked' && !task.completed);
  const completedTasks = tasks.filter(task => task.status !== 'locked' && task.completed);
  const lockedTasks = tasks.filter(task => task.status === 'locked');

  return (
    <div className="space-y-6">
      {/* Pending Quests */}
      {pendingTasks.length > 0 && (
        <div>
          <h3 className="text-xl font-semibold text-yellow-300 mb-3 flex items-center">
            <span className="mr-2">⏳</span> Active Quests
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {pendingTasks.map(task => (
              <QuestCard
                key={task.id}
                task={task}
                status="pending"
                onSelect={onSelectTask}
                onToggle={onTaskToggle}
              />
            ))}
          </div>
        </div>
      )}

      {/* Completed Quests */}
      {completedTasks.length > 0 && (
        <div>
          <h3 className="text-xl font-semibold text-green-400 mb-3 flex items-center">
            <span className="mr-2">✅</span> Completed Quests
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {completedTasks.map(task => (
              <QuestCard
                key={task.id}
                task={task}
                status="completed"
                onSelect={onSelectTask}
                onToggle={onTaskToggle}
              />
            ))}
          </div>
        </div>
      )}

      {/* Locked Quests */}
      {lockedTasks.length > 0 && (
        <div>
          <h3 className="text-xl font-semibold text-gray-400 mb-3 flex items-center">
            <span className="mr-2">🔒</span> Locked Quests
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {lockedTasks.map(task => (
              <QuestCard
                key={task.id}
                task={task}
                status="locked"
                onSelect={onSelectTask}
                onToggle={onTaskToggle}
              />
            ))}
          </div>
        </div>
      )}

      {/* Empty state */}
      {tasks.length === 0 && (
        <div className="text-center py-8">
          <div className="text-5xl mb-4">📜</div>
          <p className="text-xl text-yellow-200">No quests available yet!</p>
          <p className="text-gray-300">Complete tasks to unlock your adventure</p>
        </div>
      )}
    </div>
  );
};

export default QuestTaskList;