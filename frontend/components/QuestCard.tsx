import React, { useState } from 'react';
import { Task } from '@/types/task';

interface QuestCardProps {
  task: Task & { xp?: number; status?: string; description?: string };
  status: 'pending' | 'completed' | 'locked';
  onSelect: (task: Task) => void;
  onToggle: (taskId: number) => void;
}

const QuestCard: React.FC<QuestCardProps> = ({ task, status, onSelect, onToggle }) => {
  const [isCompleted, setIsCompleted] = useState(task.completed);
  const [showAnimation, setShowAnimation] = useState(false);

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

  return (
    <div
      className={`quest-card rounded-xl border-2 p-4 relative overflow-hidden ${getStatusColor()} transition-all duration-300 hover:scale-105 hover:shadow-lg cursor-pointer comic-panel`}
      onClick={() => (status as 'pending' | 'completed' | 'locked') !== 'locked' && onSelect(task)}
    >
      {/* Animated completion effect */}
      {showAnimation && (
        <div className="absolute inset-0 flex items-center justify-center z-10 bg-yellow-400 bg-opacity-70">
          <div className="text-4xl animate-bounce">🎉</div>
        </div>
      )}

      {/* Quest header */}
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center">
          <span className="text-2xl mr-2">{getStatusIcon()}</span>
          <h3 className={`font-bold ${(status as 'pending' | 'completed' | 'locked') === 'locked' ? 'text-gray-400' : 'text-yellow-200'}`}>
            {task.title}
          </h3>
        </div>
        {task.xp && (
          <div className="xp-display">
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
      <div className="flex justify-between items-center mt-4">
        <div className={`badge ${(status as 'pending' | 'completed' | 'locked') === 'completed' ? 'badge-completed' : (status as 'pending' | 'completed' | 'locked') === 'pending' ? 'badge-pending' : 'badge-locked'}`}>
          {(status as 'pending' | 'completed' | 'locked') === 'completed' ? 'Completed' : (status as 'pending' | 'completed' | 'locked') === 'pending' ? 'Pending' : 'Locked'}
        </div>

        {(status as 'pending' | 'completed' | 'locked') !== 'locked' ? (
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleToggle();
            }}
            disabled={(status as 'pending' | 'completed' | 'locked') === 'locked'}
            className={`
              rpg-button px-3 py-1 text-xs font-bold transition-all
              ${isCompleted
                ? 'bg-green-600 hover:bg-green-700 text-white'
                : 'bg-yellow-600 hover:bg-yellow-700 text-yellow-900'}
              ${(status as 'pending' | 'completed' | 'locked') === 'locked' ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            {isCompleted ? 'Completed!' : 'Accept Quest'}
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