import React, { useState, useEffect, useRef } from 'react';
import { chatService } from '../lib/chat-api';
import { Message } from '../types/task';
import ReactMarkdown from 'react-markdown';

interface ChatLayerProps {
  onMutationSuccess: () => void;
}

const ChatLayer: React.FC<ChatLayerProps> = ({ onMutationSuccess }) => {
  const [messages, setMessages] = useState<Partial<Message>[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize conversation ID
  useEffect(() => {
    const savedId = localStorage.getItem('current_conversation_id');
    const newId = savedId || crypto.randomUUID();
    setConversationId(newId);
    localStorage.setItem('current_conversation_id', newId);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg: Partial<Message> = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    const currentInput = input;
    setInput('');
    setLoading(true);

    try {
      const response = await chatService.sendMessage({
        message: currentInput,
        conversation_id: conversationId,
      });

      setMessages(prev => [...prev, { role: 'assistant', content: response }]);

      // Simple heuristic for mutation success visibility:
      // if the agent confirms an action, refresh the sidebar.
      const lowerResp = response.toLowerCase();
      if (
        lowerResp.includes("created") ||
        lowerResp.includes("deleted") ||
        lowerResp.includes("updated") ||
        lowerResp.includes("completed")
      ) {
        onMutationSuccess();
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Error: Unable to reach the AI Agent." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] border rounded-lg bg-white shadow-sm">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-lg ${
              msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-800'
            }`}>
              <ReactMarkdown>
                {msg.content || ''}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="p-4 border-t flex space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me to add, list, complete, or delete tasks..."
          className="flex-1 border rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={loading}
        />
        <button
          type="submit"
          className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:bg-indigo-300"
          disabled={loading || !input.trim()}
        >
          {loading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatLayer;
