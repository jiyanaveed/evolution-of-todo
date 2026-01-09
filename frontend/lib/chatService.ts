/**
 * chatService.ts - Phase 3 Communication Layer
 * Manages the stateless connection between the UI and the orchestrated /chat backend.
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface MessageResponse {
  role: 'user' | 'assistant';
  content: string;
}

export const chatService = {
  /**
   * Sends user intent to the AI Agent.
   * RULE: [Ownership] Implicitly injected via Authorization header.
   */
  async sendMessage(message: string, conversationId: string) {
    const token = localStorage.getItem('access_token');

    const response = await axios.post<string>(
      `${API_BASE_URL}/chat`,
      { message, conversation_id: conversationId },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    const content = response.data;

    // RULE: [Dynamic Sync] Detect if the agent confirmed a successful task mutation.
    const isMutationConfirmed = this._checkMutation(content);

    return { content, isMutationConfirmed };
  },

  /**
   * RULE: [Stateless Fetch] Retrieve verbatim history from the DB on mount.
   */
  async getHistory(conversationId: string): Promise<MessageResponse[]> {
    const token = localStorage.getItem('access_token');
    const response = await axios.get(`${API_BASE_URL}/chat/history/${conversationId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },

  _checkMutation(text: string): boolean {
    const lower = text.toLowerCase();
    return ["created", "deleted", "updated", "completed", "renamed"].some(k => lower.includes(k));
  }
};
