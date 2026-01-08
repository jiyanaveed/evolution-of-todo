import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { chatService, MessageResponse } from '../lib/chatService';

interface ChatBoxProps {
  conversationId: string;
  onMutationSuccess: () => void;
}

/**
 * ChatBox.tsx - Interface for orchestrated AI task management.
 * RULE: [Stateless Fetch] History is retrieved on mount.
 * RULE: [Two-Step Mutation] Visual confirmation feedback.
 * RULE: [Verbatim Persistence] No local summarization.
 */
const ChatBox: React.FC<ChatBoxProps> = ({ conversationId, onMutationSuccess }) => {
  const [messages, setMessages] = useState<MessageResponse[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isConfirming, setIsConfirming] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  // RULE: [Stateless Fetch] Retrieve existing history for the session.
  useEffect(() => {
    chatService.getHistory(conversationId).then(setMessages).catch(console.error);
  }, [conversationId]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const onSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input;
    setInput('');
    setLoading(true);

    // RULE: [Verbatim] Display exactly what the user sent.
    setMessages(p => [...p, { role: 'user', content: userText }]);

    try {
      const { content, isMutationConfirmed } = await chatService.sendMessage(userText, conversationId);

      // RULE: [Verbatim] Display exactly what the agent returned.
      setMessages(p => [...p, { role: 'assistant', content }]);

      // RULE: [Two-Step Mutation] Detect confirmation prompt.
      setIsConfirming(content.toLowerCase().includes("are you sure"));

      // RULE: [Dynamic Sync] Trigger sidebar refresh on confirmed action.
      if (isMutationConfirmed) onMutationSuccess();

    } catch (err: any) {
      setMessages(p => [...p, { role: 'assistant', content: err.message || "System error." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[550px] border border-gray-200 rounded-xl bg-white shadow-lg overflow-hidden">
      <div className="flex-1 overflow-y-auto p-5 space-y-4">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm ${
              m.role === 'user' ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-gray-100 text-gray-800 rounded-tl-none'
            }`}>
              <ReactMarkdown>
                {m.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        <div ref={endRef} />
      </div>

      <form onSubmit={onSend} className={`p-4 border-t transition-colors ${isConfirming ? 'bg-amber-50' : 'bg-gray-50'}`}>
        {isConfirming && <div className="text-[10px] font-bold text-amber-600 mb-2 uppercase tracking-tight">Warning: Confirmation Required</div>}
        <div className="flex gap-2">
          <input
            className={`flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 ${isConfirming ? 'border-amber-300 focus:ring-amber-500' : 'border-gray-300 focus:ring-indigo-500'}`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={isConfirming ? "Please reply Yes or No" : "Manage tasks with AI..."}
            disabled={loading}
          />
          <button
            className={`px-5 py-2 rounded-lg font-medium transition-opacity disabled:opacity-50 ${isConfirming ? 'bg-amber-600 text-white' : 'bg-indigo-600 text-white'}`}
            type="submit"
            disabled={loading || !input.trim()}
          >
            {isConfirming ? 'Confirm' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatBox;
