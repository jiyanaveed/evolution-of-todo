/**
 * Empty State Component
 * Shows when there are no messages in the chat
 */

import React from 'react';

interface EmptyStateProps {
  title?: string;
  subtitle?: string;
  children?: React.ReactNode;
}

export default function EmptyState({ title = "No messages yet", subtitle = "Start a conversation with the AI assistant", children }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center py-12">
      <div className="mb-6 p-4 bg-indigo-100 rounded-full">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
      </div>
      <h3 className="text-xl font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-gray-600 max-w-md">{subtitle}</p>
      {children && <div className="mt-4">{children}</div>}
    </div>
  );
}