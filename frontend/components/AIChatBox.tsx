/**
 * Enhanced AI Chat Component with improved UI/UX
 * Following the requirements for a production-grade chatbot UI similar to ChatGPT
 */
'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import EmptyState from './EmptyState';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

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
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const endRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();

  // Initialize conversation ID
  useEffect(() => {
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

  const handleSend = async (message: string) => {
    if (!message.trim() || isLoading || !user) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: message.trim(),
      createdAt: new Date(),
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, userMessage]);

    setIsLoading(true);

    try {
      const token = getToken();

      // Get the API base URL from environment variable
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

      // Ensure the base URL doesn't have a trailing slash for proper concatenation
      const normalizedBaseUrl = apiBaseUrl.endsWith('/') ? apiBaseUrl.slice(0, -1) : apiBaseUrl;

      // Call the backend API endpoint
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
          message: message.trim(),
          ...(currentConversationId && { conversation_id: currentConversationId }),
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API request failed with status ${response.status}: ${errorText}`);
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
        content: `Sorry, I encountered an error processing your request: ${(error as Error).message}. Please try again.`,
        createdAt: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-gradient-to-b from-gray-50 to-white">
        {messages.length === 0 && (
          <EmptyState
            title="Welcome to TaskFlow AI"
            subtitle="I'm your AI assistant for managing tasks. You can ask me to create, update, or manage your tasks using natural language."
          >
            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3 max-w-lg">
              <div className="bg-gray-100 rounded-lg p-3 text-sm">
                <span className="font-medium">Try:</span> "Add buy groceries"
              </div>
              <div className="bg-gray-100 rounded-lg p-3 text-sm">
                <span className="font-medium">Try:</span> "Show my tasks"
              </div>
              <div className="bg-gray-100 rounded-lg p-3 text-sm">
                <span className="font-medium">Try:</span> "Complete task 1"
              </div>
              <div className="bg-gray-100 rounded-lg p-3 text-sm">
                <span className="font-medium">Try:</span> "Delete task 2"
              </div>
            </div>
          </EmptyState>
        )}

        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            role={message.role}
            content={message.content}
          />
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl rounded-bl-none px-4 py-3 text-sm max-w-[85%]">
              <div className="flex items-center">
                <div className="flex space-x-1">
                  <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
                <span className="ml-2 text-gray-500">Thinking...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4">
        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </div>
    </div>
  );
}