import React, { useState, useRef, useEffect } from 'react';
import styles from './Chatbot.module.css';

interface Message {
  id: string;
  sender: 'user' | 'bot';
  content: string | string[];
  timestamp: Date;
}

interface BackendResponse {
  answer?: string;
  error?: string;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'bot',
      content: 'Hello! I\'m your stock analysis assistant. Ask me about any stock to get analysis and recommendations.',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Helper function to parse backend response
  const parseResponse = (data: BackendResponse): string | string[] => {
    if (data.answer) {
      return data.answer;
    }
    if (data.error) {
      return `Error: ${data.error}`;
    }

    return 'I could not process your request. Please try again.';
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: input }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const parsedResponse = parseResponse(data);
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'bot',
        content: parsedResponse,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        sender: 'bot',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to fetch response from server'}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.chatbotHeader}>
        <h2 className={styles.title}>Stock Analysis Assistant</h2>
        <p className={styles.subtitle}>Get AI-powered stock insights</p>
      </div>

      <div className={styles.messagesContainer}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.message} ${styles[message.sender]}`}
          >
            <div className={styles.messageBubble}>
              {typeof message.content === 'string' ? (
                <p className={styles.messageText}>{message.content}</p>
              ) : (
                <div className={styles.messageContent}>
                  {message.content.map((text, idx) => (
                    <p key={idx} className={styles.messageText}>
                      {text}
                    </p>
                  ))}
                </div>
              )}
              <span className={styles.timestamp}>
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </span>
            </div>
          </div>
        ))}
        {loading && (
          <div className={`${styles.message} ${styles.bot}`}>
            <div className={styles.messageBubble}>
              <div className={styles.loadingDots}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} className={styles.inputForm}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about a stock... (e.g., 'Tell me about AAPL')"
          className={styles.input}
          disabled={loading}
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={loading || !input.trim()}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default Chatbot;
