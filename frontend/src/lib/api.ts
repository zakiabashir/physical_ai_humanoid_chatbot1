/**
 * API Client for AI-Native Textbook Platform
 *
 * Handles communication with backend services:
 * - Auth Service
 * - Chatbot Service
 * - Personalization Service
 */

// API URLs from environment variables
const AUTH_API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL || '';
const CHATBOT_API_URL = process.env.NEXT_PUBLIC_CHATBOT_API_URL || '';
const PERSONALIZATION_API_URL = process.env.NEXT_PUBLIC_PERSONALIZATION_API_URL || '';

// Types
export interface User {
  id: string;
  email: string;
  name?: string;
  preferred_language: 'en' | 'ur';
  created_at: string;
}

export interface ChatRequest {
  question: string;
  selected_text?: string;
  language: 'en' | 'ur';
}

export interface ChatResponse {
  answer: string;
  sources: Array<{
    chapter_id: string;
    section_title: string;
    content: string;
  }>;
  language: string;
}

export interface ProgressRecord {
  id: string;
  user_id: string;
  chapter_id: string;
  status: 'not_started' | 'in_progress' | 'completed';
  last_position?: number;
  completed_at?: string;
}

export interface Bookmark {
  id: string;
  user_id: string;
  chapter_id: string;
  section_id: string;
  note?: string;
  created_at: string;
}

export interface Recommendation {
  chapter_id: string;
  title: string;
  reason: string;
}

// Auth API
export const authApi = {
  async signup(email: string, password: string, name?: string) {
    const response = await fetch(`${AUTH_API_URL}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Signup failed');
    return response.json();
  },

  async login(email: string, password: string) {
    const response = await fetch(`${AUTH_API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Login failed');
    return response.json();
  },

  async logout() {
    const response = await fetch(`${AUTH_API_URL}/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Logout failed');
    return response.json();
  },

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${AUTH_API_URL}/users/me`, {
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Failed to get user');
    return response.json();
  },

  getOAuthUrl(provider: 'google' | 'github') {
    return `${AUTH_API_URL}/auth/oauth/${provider}`;
  },
};

// Chatbot API
export const chatbotApi = {
  async askQuestion(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${CHATBOT_API_URL}/chat/question`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });
    if (!response.ok) throw new Error('Chat request failed');
    return response.json();
  },
};

// Personalization API
export const personalizationApi = {
  // Progress
  async getProgress(): Promise<ProgressRecord[]> {
    const response = await fetch(`${PERSONALIZATION_API_URL}/progress`, {
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Failed to get progress');
    return response.json();
  },

  async updateProgress(chapterId: string, status: string, lastPosition?: number) {
    const response = await fetch(`${PERSONALIZATION_API_URL}/progress/${chapterId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ status, last_position: lastPosition }),
    });
    if (!response.ok) throw new Error('Failed to update progress');
    return response.json();
  },

  // Bookmarks
  async getBookmarks(): Promise<Bookmark[]> {
    const response = await fetch(`${PERSONALIZATION_API_URL}/bookmarks`, {
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Failed to get bookmarks');
    return response.json();
  },

  async createBookmark(chapterId: string, sectionId: string, note?: string): Promise<Bookmark> {
    const response = await fetch(`${PERSONALIZATION_API_URL}/bookmarks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ chapter_id: chapterId, section_id: sectionId, note }),
    });
    if (!response.ok) throw new Error('Failed to create bookmark');
    return response.json();
  },

  async deleteBookmark(bookmarkId: string) {
    const response = await fetch(`${PERSONALIZATION_API_URL}/bookmarks/${bookmarkId}`, {
      method: 'DELETE',
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Failed to delete bookmark');
    return response.json();
  },

  // Recommendations
  async getRecommendations(): Promise<Recommendation[]> {
    const response = await fetch(`${PERSONALIZATION_API_URL}/recommendations`, {
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Failed to get recommendations');
    return response.json();
  },
};

export default {
  auth: authApi,
  chatbot: chatbotApi,
  personalization: personalizationApi,
};
