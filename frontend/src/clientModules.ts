/**
 * Client-side module for exposing environment variables
 * These are available in the browser at runtime
 */

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      readonly NEXT_PUBLIC_AUTH_API_URL?: string;
      readonly NEXT_PUBLIC_CHATBOT_API_URL?: string;
      readonly NEXT_PUBLIC_PERSONALIZATION_API_URL?: string;
    }
  }
}

export const API_ENDPOINTS = {
  auth: process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8001',
  chatbot: process.env.NEXT_PUBLIC_CHATBOT_API_URL || 'http://localhost:8002',
  personalization: process.env.NEXT_PUBLIC_PERSONALIZATION_API_URL || 'http://localhost:8003',
};

export {};
