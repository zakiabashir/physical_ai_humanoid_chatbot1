/**
 * ChatbotWidget Component
 *
 * Floating chat widget for RAG-based Q&A about textbook content
 */

import React, { useState, useRef, useEffect } from 'react';
import { chatbotApi, ChatResponse } from '../lib/api';

export default function ChatbotWidget(): React.JSX.Element {
  const [isOpen, setIsOpen] = useState(false);
  const [question, setQuestion] = useState('');
  const [conversation, setConversation] = useState<Array<{role: 'user' | 'assistant', content: string}>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversation]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;

    const userMessage = question;
    setQuestion('');
    setConversation(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // Detect language from first character (Urdu = RTL)
      const isUrdu = /[\u0600-\u06FF]/.test(userMessage);
      const response: ChatResponse = await chatbotApi.askQuestion({
        question: userMessage,
        language: isUrdu ? 'ur' : 'en',
      });

      setConversation(prev => [...prev, {
        role: 'assistant',
        content: response.answer
      }]);
    } catch (error) {
      setConversation(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I couldn\'t process your question. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Floating Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`chatbot-toggle ${isOpen ? 'open' : ''}`}
        aria-label="Toggle chatbot"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          {isOpen ? (
            <path d="M18 6L6 18M6 6l12 12" /> // Close icon
          ) : (
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /> // Chat icon
          )}
        </svg>
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-widget">
          <div className="chatbot-header">
            <h3>Ask AI</h3>
            <p>Questions about Physical AI?</p>
          </div>

          <div className="chatbot-messages">
            {conversation.length === 0 && (
              <div className="chatbot-welcome">
                <p>Hi! I'm your AI textbook assistant.</p>
                <p>Ask me anything about Physical AI, ROS 2, Gazebo, or humanoid robotics!</p>
              </div>
            )}
            {conversation.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-content typing">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="chatbot-input">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading || !question.trim()}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
