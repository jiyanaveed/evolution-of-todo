/**
 * ConversationList Component
 * Optional component for showing conversation history
 */
import React from 'react';

interface Conversation {
  id: number;
  title: string;
  lastMessage: string;
  timestamp: string;
}

interface ConversationListProps {
  conversations: Conversation[];
  onSelect: (id: number) => void;
  selectedId?: number;
}

export default function ConversationList({ conversations, onSelect, selectedId }: ConversationListProps) {
  return (
    <div className="border-r border-gray-200 w-64 bg-white min-h-full">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800">Conversations</h3>
      </div>
      <div className="overflow-y-auto">
        {conversations.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            No conversations yet
          </div>
        ) : (
          <ul>
            {conversations.map((conv) => (
              <li key={conv.id}>
                <button
                  onClick={() => onSelect(conv.id)}
                  className={`w-full text-left p-4 hover:bg-gray-50 transition-colors ${
                    selectedId === conv.id ? 'bg-indigo-50 border-l-4 border-indigo-500' : ''
                  }`}
                >
                  <div className="font-medium text-gray-900 truncate">{conv.title}</div>
                  <div className="text-sm text-gray-500 truncate mt-1">{conv.lastMessage}</div>
                  <div className="text-xs text-gray-400 mt-1">{conv.timestamp}</div>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}