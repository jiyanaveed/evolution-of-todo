import React, { useState, useEffect } from 'react';
import { Task } from '@/types/task';

interface QuestCardProps {
  task: Task & { xp?: number; status?: string; description?: string };
  status: 'pending' | 'completed' | 'locked';
  onSelect: (task: Task) => void;
  onToggle: (taskId: number) => void;
  /** Compact, no grow-on-hover — for dashboard column layout */
  embed?: boolean;
}

const QuestCard: React.FC<QuestCardProps> = ({ task, status, onSelect, onToggle, embed = false }) => {
  const [isCompleted, setIsCompleted] = useState(task.completed);
  const [showAnimation, setShowAnimation] = useState(false);

  useEffect(() => {
    setIsCompleted(task.completed);
  }, [task.completed, task.id]);

  const handleToggle = () => {
    if (status === 'locked') return;

    if (!isCompleted) {
      setShowAnimation(true);
      setTimeout(() => {
        onToggle(task.id);
        setIsCompleted(true);
      }, 500);
    } else {
      onToggle(task.id);
      setIsCompleted(false);
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'completed': return 'border-green-500 bg-green-900 bg-opacity-30';
      case 'pending': return 'border-yellow-500 bg-yellow-900 bg-opacity-30';
      case 'locked': return 'border-gray-500 bg-gray-900 bg-opacity-30';
      default: return 'border-gray-600 bg-gray-800';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'completed': return '✅';
      case 'pending': return '⚔️';
      case 'locked': return '🔒';
      default: return '❓';
    }
  };

  const shell = embed
    ? 'rounded-xl border-2 p-3 sm:p-4 relative overflow-hidden min-w-0 w-full max-w-full cursor-default'
    : 'quest-card rounded-xl border-2 p-4 relative overflow-hidden';
  const hover = embed
    ? ' transition-shadow duration-200 hover:shadow-md'
    : ' transition-all duration-300 hover:scale-105 hover:shadow-lg cursor-pointer comic-panel';

  return (
    <div
      className={`${shell} ${getStatusColor()} ${hover}`}
      onClick={() => !embed && (status as 'pending' | 'completed' | 'locked') !== 'locked' && onSelect(task)}
    >
      {/* Animated completion effect */}
      {showAnimation && (
        <div className="absolute inset-0 flex items-center justify-center z-10 bg-yellow-400 bg-opacity-70">
          <div className="text-4xl animate-bounce">🎉</div>
        </div>
      )}

      {/* Quest header */}
      <div className="flex justify-between items-start gap-2 mb-2 min-w-0">
        <div className="flex items-start min-w-0 flex-1">
          <span className="text-xl sm:text-2xl mr-2 shrink-0 leading-none pt-0.5">{getStatusIcon()}</span>
          <h3
            className={`font-bold break-words min-w-0 pr-1 ${
              (status as 'pending' | 'completed' | 'locked') === 'locked' ? 'text-gray-400' : 'text-yellow-200'
            }`}
          >
            {task.title}
          </h3>
        </div>
        {task.xp && (
          <div className="xp-display text-xs sm:text-sm shrink-0 whitespace-nowrap">
            +{task.xp} XP
          </div>
        )}
      </div>

      {/* Quest description */}
      {task.description && (
        <p className={`text-sm mb-3 ${(status as 'pending' | 'completed' | 'locked') === 'locked' ? 'text-gray-500' : 'text-gray-300'}`}>
          {task.description}
        </p>
      )}

      {/* Quest status and actions */}
      <div className="flex flex-col sm:flex-row flex-wrap sm:flex-nowrap justify-between items-stretch sm:items-center gap-2 mt-4 min-w-0">
        <div
          className={`badge text-xs min-w-0 break-words ${(status as 'pending' | 'completed' | 'locked') === 'completed' ? 'badge-completed' : (status as 'pending' | 'completed' | 'locked') === 'pending' ? 'badge-pending' : 'badge-locked'}`}
        >
          {(status as 'pending' | 'completed' | 'locked') === 'completed'
            ? 'Completed'
            : (status as 'pending' | 'completed' | 'locked') === 'pending'
              ? 'Pending'
              : 'Locked'}
        </div>

        {(status as 'pending' | 'completed' | 'locked') !== 'locked' ? (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              handleToggle();
            }}
            disabled={(status as 'pending' | 'completed' | 'locked') === 'locked'}
            className={`
              rpg-button px-2.5 sm:px-3 py-1.5 text-xs font-bold transition-all shrink-0 max-w-full
              ${isCompleted ? 'bg-green-600 hover:bg-green-700 text-white' : 'bg-yellow-600 hover:bg-yellow-700 text-yellow-900'}
              ${(status as 'pending' | 'completed' | 'locked') === 'locked' ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            {isCompleted ? 'Reopen' : 'Complete quest'}
          </button>
        ) : (
          <div className="text-xs text-gray-500 italic">Complete prerequisites</div>
        )}
      </div>

      {/* Decorative elements */}
      <div className="absolute top-2 right-2 opacity-20">
        {status === 'completed' ? '⚔️' : status === 'pending' ? '🛡️' : '🔮'}
      </div>
    </div>
  );
};

export default QuestCard;