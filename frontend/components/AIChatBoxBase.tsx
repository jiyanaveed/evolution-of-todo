/**
 * AI Chat Component using direct API calls to backend
 * Phase 3: OpenAI ChatKit Implementation
 */
'use client';

import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { useAuth } from '../contexts/AuthContext';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  createdAt: Date;
}

interface ChatBoxProps {
  conversationId: string;
  onMutationSuccess: () => void;
}

export default function AIChatBox({ conversationId, onMutationSuccess }: ChatBoxProps) {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const endRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();

  // Initialize conversation ID
  useEffect(() => {
    // Convert the conversationId prop to a number, defaulting to null if invalid
    if (!conversationId || conversationId === '') {
      setCurrentConversationId(null); // Will create new conversation
    } else {
      const id = parseInt(conversationId);
      if (!isNaN(id) && id > 0) {
        setCurrentConversationId(id);
      } else {
        setCurrentConversationId(null); // Will create new conversation
      }
    }
  }, [conversationId]);

  // Scroll to bottom when messages change
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const getToken = () => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('better-auth.session_token');
    }
    return null;
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading || !user) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      createdAt: new Date(),
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, userMessage]);
    const userInput = input;
    setInput('');
    setIsLoading(true);

    try {
      const token = getToken();

      // Get the API base URL from environment variable
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

      // Ensure the base URL doesn't have a trailing slash for proper concatenation
      const normalizedBaseUrl = apiBaseUrl.endsWith('/') ? apiBaseUrl.slice(0, -1) : apiBaseUrl;

      // Call the new backend API endpoint
      const url = `${normalizedBaseUrl}/api/${user.id}/chat`;
      console.log('[DEBUG] Calling API:', url);
      console.log('[DEBUG] User ID:', user.id);
      console.log('[DEBUG] Token present:', !!token);
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` }),
        },
        body: JSON.stringify({
          message: userInput,
          ...(currentConversationId && { conversation_id: currentConversationId }),
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if a new one was created by the backend
      if (data.conversation_id && currentConversationId !== data.conversation_id) {
        setCurrentConversationId(data.conversation_id);
      }

      // Add assistant response to messages
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        createdAt: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Check if the response indicates a task mutation to trigger refresh
      const content = data.response.toLowerCase();
      if (content.includes('created') || content.includes('deleted') ||
          content.includes('updated') || content.includes('completed') ||
          content.includes('renamed')) {
        onMutationSuccess();
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        createdAt: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[550px] border border-gray-200 rounded-xl bg-white shadow-lg overflow-hidden">
      <div className="flex-1 overflow-y-auto p-5 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-lg">Start a conversation with your AI assistant</p>
            <p className="text-sm mt-2">Try: &quot;list my tasks&quot; or &quot;add buy groceries&quot;</p>
          </div>
        )}
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm ${
              m.role === 'user'
                ? 'bg-indigo-600 text-white rounded-tr-none'
                : 'bg-gray-100 text-gray-800 rounded-tl-none'
            }`}>
              <ReactMarkdown>{m.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl rounded-tl-none px-4 py-2 text-sm">
              <span className="animate-pulse">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      <form onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="p-4 border-t bg-gray-50">
        <div className="flex gap-2">
          <input
            name="content"
            ref={(el) => {
              if (el) el.dataset.testid = 'chat-input';
            }}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Manage tasks with AI..."
            disabled={isLoading}
          />
          {isLoading ? (
            <button
              type="button"
              className="px-5 py-2 rounded-lg font-medium bg-gray-400 text-white"
              disabled
            >
              Sending...
            </button>
          ) : (
            <button
              type="submit"
              className="px-5 py-2 rounded-lg font-medium bg-indigo-600 text-white hover:bg-indigo-700"
              disabled={!input.trim() || isLoading}
            >
              Send
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

// Note: This component assumes the useAuth hook is available from the AuthContext
// If not available, you'll need to import it: import { useAuth } from '../contexts/AuthContext';
