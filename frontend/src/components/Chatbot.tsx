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
  response?: string;
  error?: string;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'bot',
      content: '👋 Welcome to the Risk-Aware Trading Assistant! I analyze stocks using a multi-agent consensus system. Ask me about TCS, RELIANCE, or HDFCBANK to see our risk assessment in action.',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Helper function to parse backend response
  const parseResponse = (data: BackendResponse): string | string[] => {
    if (data.response) {
      return data.response;
    }
    if (data.answer) {
      return data.answer;
    }
    if (data.error) {
      return `⚠️ Error: ${data.error}`;
    }

    return '⚠️ I could not process your request. Please try again.';
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
      const response = await fetch('http://localhost:5001/api/chat', {
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
        content: `⚠️ Connection Error: Unable to reach the backend server. The simulation engine is working, but the chatbot API is currently unavailable.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  // Quick action buttons
  const quickActions = [
    { label: '📊 TCS Analysis', query: 'What is the verdict for TCS?' },
    { label: '💼 RELIANCE Status', query: 'What is the verdict for RELIANCE?' },
    { label: '🏦 HDFCBANK Risk', query: 'What is the verdict for HDFCBANK?' },
  ];

  const handleQuickAction = (query: string) => {
    setInput(query);
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.chatbotHeader}>
        <div className={styles.headerContent}>
          <div className={styles.logoContainer}>
            <div className={styles.logo}>📈</div>
            <div>
              <h2 className={styles.title}>Risk-Aware Trading AI</h2>
              <p className={styles.subtitle}>Multi-Agent Consensus System</p>
            </div>
          </div>
          <div className={styles.statusBadge}>
            <span className={styles.statusDot}></span>
            <span>Live</span>
          </div>
        </div>
      </div>

      <div className={styles.messagesContainer}>
        {messages.length === 1 && (
          <div className={styles.quickActionsContainer}>
            <p className={styles.quickActionsTitle}>Try asking about:</p>
            <div className={styles.quickActions}>
              {quickActions.map((action, idx) => (
                <button
                  key={idx}
                  className={styles.quickActionBtn}
                  onClick={() => handleQuickAction(action.query)}
                >
                  {action.label}
                </button>
              ))}
            </div>
          </div>
        )}

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
              <p className={styles.loadingText}>Analyzing with 5 AI agents...</p>
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
          placeholder="Ask about stock risk levels... (e.g., 'What is the verdict for TCS?')"
          className={styles.input}
          disabled={loading}
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={loading || !input.trim()}
        >
          {loading ? '⏳' : '🚀'} {loading ? 'Analyzing' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default Chatbot;
