/**
 * Chat Container Component
 * Wraps the AIChatBox with proper layout and structure
 */
'use client';

import React from 'react';
import AIChatBox from './AIChatBox'; // Updated path

interface ChatContainerProps {
  conversationId: string;
  onMutationSuccess: () => void;
}

export default function ChatContainer({ conversationId, onMutationSuccess }: ChatContainerProps) {
  return (
    <div className="flex flex-col h-[calc(100vh-200px)] min-h-[500px]">
      <div className="flex-1 overflow-hidden">
        <AIChatBox
          conversationId={conversationId}
          onMutationSuccess={onMutationSuccess}
        />
      </div>
    </div>
  );
}