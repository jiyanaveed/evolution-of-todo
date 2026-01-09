import React from 'react';
import { Task } from '@/types/task';

interface QuestMapProps {
  tasks: Array<Task & { xp?: number; status?: string; description?: string }>;
  heroPosition: number;
}

const QuestMap: React.FC<QuestMapProps> = ({ tasks, heroPosition }) => {
  // Calculate positions for each task on the map
  const taskPositions = tasks.map((task, index) => ({
    ...task,
    position: index,
    isAccessible: task.status !== 'locked',
    isCompleted: task.completed
  }));

  return (
    <div className="relative w-full h-48 sm:h-64 quest-path overflow-hidden rounded-xl">
      {/* Path */}
      <div className="absolute top-1/2 left-0 right-0 h-5 bg-gradient-to-r from-yellow-700 via-yellow-600 to-yellow-700 transform -translate-y-1/2 z-0 rounded-full"></div>

      {/* Tasks/Quests along the path */}
      {taskPositions.map((task, index) => {
        const leftPercent = (index / Math.max(tasks.length - 1, 1)) * 100;
        const isCurrent = index === heroPosition;
        const isPast = index < heroPosition;

        return (
          <div
            key={task.id}
            className={`absolute top-1/2 transform -translate-y-1/2 -translate-x-1/2 z-10 transition-all duration-500 ${
              task.status === 'locked' ? 'opacity-50 grayscale' : ''
            } ${isCurrent ? 'scale-125 z-20' : ''}`}
            style={{ left: `${leftPercent}%` }}
          >
            {/* Quest marker */}
            <div className={`
              w-12 h-12 sm:w-16 sm:h-16 rounded-full flex items-center justify-center border-4
              ${task.status === 'locked'
                ? 'bg-gray-600 border-gray-400 cursor-not-allowed'
                : task.completed
                  ? 'bg-green-600 border-green-400'
                  : 'bg-yellow-600 border-yellow-400'}
              relative shadow-lg
            `}>
              {task.status !== 'locked' && (
                <span className="text-lg sm:text-xl">
                  {task.completed ? '✅' : '⚔️'}
                </span>
              )}
              {task.status === 'locked' && (
                <span className="text-lg sm:text-xl">🔒</span>
              )}

              {/* Quest info tooltip */}
              <div className="absolute -top-20 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-80 text-white text-xs p-2 rounded-lg min-w-max opacity-0 hover:opacity-100 transition-opacity z-30 whitespace-nowrap">
                <div className="font-bold">{task.title}</div>
                <div>XP: {task.xp || 0}</div>
                {task.description && <div className="text-xs mt-1">{task.description}</div>}
              </div>
            </div>

            {/* Quest label */}
            <div className="hidden sm:block text-center mt-2 text-xs font-bold text-yellow-200 bg-black bg-opacity-50 px-2 py-1 rounded whitespace-nowrap">
              {task.title}
            </div>
          </div>
        );
      })}

      {/* Hero avatar - only show if there are tasks */}
      {tasks.length > 0 && (
        <div
          className="absolute top-1/2 transform -translate-y-1/2 -translate-x-1/2 z-20 transition-all duration-1000 ease-in-out hero-avatar"
          style={{
            left: `${(heroPosition / Math.max(tasks.length - 1, 1)) * 100}%`
          }}
        >
          <div className="relative">
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-blue-500 rounded-full flex items-center justify-center border-4 border-yellow-400">
              <span className="text-xl sm:text-2xl">🧙</span>
            </div>
            <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-4 h-4 bg-yellow-400 rounded-full animate-bounce"></div>
          </div>
        </div>
      )}

      {/* Decorative elements */}
      <div className="absolute top-2 left-4 sm:top-4 sm:left-10 text-xl sm:text-3xl">🌳</div>
      <div className="absolute top-4 right-6 sm:top-8 sm:right-20 text-xl sm:text-3xl">🏰</div>
      <div className="absolute bottom-4 left-1/4 sm:bottom-6 sm:left-1/3 text-xl sm:text-3xl">🗡️</div>
      <div className="absolute bottom-6 right-1/4 sm:bottom-10 sm:right-1/4 text-xl sm:text-3xl">💰</div>
    </div>
  );
};

export default QuestMap;