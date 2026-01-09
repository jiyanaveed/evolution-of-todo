import api from './api';
import { Message, ChatRequest } from '../types/task';

export const chatService = {
  /**
   * Send a message to the AI Agent and receive the orchestrated response.
   * FETCH -> APPEND -> RUN -> PERSIST -> RESPOND lifecycle handled on backend.
   */
  async sendMessage(request: ChatRequest): Promise<string> {
    const response = await api.post<string>('/chat', request);
    return response.data;
  },

  /**
   * Retrieve verbatim conversation history for a given conversation.
   * Note: The current backend implementation handles history internally during /chat,
   * but we might need a fetch for UI initialization.
   */
  async getHistory(conversationId: string): Promise<Message[]> {
    // This assumes a backend endpoint GET /mcp/history/{cid} exists or needs to be added
    // For Phase 3 initial sync, history is persisted in the DB and managed by the agent.
    // If a specific history fetch endpoint is missing, we'll rely on the /chat flow.
    const response = await api.get<Message[]>(`/mcp/history/${conversationId}`);
    return response.data;
  },
};
