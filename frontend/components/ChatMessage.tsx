/**
 * ChatMessage Component
 * Displays individual chat messages with proper styling
 */
import React from 'react';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatMessage({ role, content }: ChatMessageProps) {
  return (
    <div className={`flex ${role === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-sm ${
          role === 'user'
            ? 'bg-indigo-600 text-white rounded-br-none'
            : 'bg-gray-100 text-gray-800 rounded-bl-none'
        }`}
      >
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown
            components={{
              p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
              ul: ({node, ...props}) => <ul className="list-disc pl-5 mb-2" {...props} />,
              ol: ({node, ...props}) => <ol className="list-decimal pl-5 mb-2" {...props} />,
              li: ({node, ...props}) => <li className="mb-1" {...props} />,
              strong: ({node, ...props}) => <strong className="font-semibold" {...props} />,
              em: ({node, ...props}) => <em className="italic" {...props} />,
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}