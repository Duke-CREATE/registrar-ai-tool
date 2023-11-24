// app/page.tsx
'use client';
import React, { useRef, useState } from 'react';
import './styles/page.css';

// ===============
// =============== CHAT RECOMMENDATIONS ===============
// ===============

// Recommendation
// Description: A recommendation that is displayed in a box. Takes 'recommendation' as a prop.
// Contains: None
// Props: recommendation
interface RecommendationProps {
  recommendation: string;
}
function Recommendation({ recommendation }: RecommendationProps) {
  return (
    <div className="recommendation-box">
      <p className="recommendation-text">{recommendation}</p>
    </div>
  );
}

// InputRecommendations
// Description: A field for displaying recommendations.
// Contains: 4 Recommendation
// Props: None
function InputRecommendations() {
  const recommendations = [
    "Courses that teach machine learning",
    "Courses about product management",
    "Fintech courses on Tuesdays and Thursdays",
    "Environmental engineering courses",
  ];

  return (
    <div className="input-recommendations">
      {recommendations.map((rec, index) => (
        <Recommendation key={index} recommendation={rec} />
      ))}
    </div>
  );
}

// ===============
// =============== CHAT INTERFACE ===============
// ===============

// ChatWindow
// Description: Where user's sent input and system responses are displayed.
// Contains: None
// Props: None
function ChatInterface() {
  const [messages, setMessages] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSendMessage = () => {
    console.log('handleSendMessage called'); // Debugging log
    if (inputRef.current && inputRef.current.value.trim() !== '') {
      const message = inputRef.current.value;
      setMessages(prevMessages => {
        console.log('New message:', message); // Debugging log for new message
        return [...prevMessages, message];
      });
      inputRef.current.value = '';
    } else {
      console.log('Input is empty or ref is not set'); // Debugging log for empty input
    }
  };

  console.log('Messages to render:', messages); // Debugging log for messages array

  return (
      <div className="chat-interface">
          <div className="send-chat-field">
              <input type="text" className="chat-input" ref={inputRef} />
              <button className="chat-input-button" onClick={() => console.log('Button clicked')}>
                Send
              </button>
          </div>
          <div>
              <InputRecommendations />
          </div>
          <div className="chat-window">
              {messages.map((message, index) => (
                  <p key={index}>{message}</p>
              ))}
          </div>
      </div>
  );
}


// ===============
// =============== PAGE ===============
// ===============

// Page
// Description: The page that contains the chat interface
// Contains: ChatInterface
// Props: None
export default function Page() {
  return (
    <div className="main-content">
      <ChatInterface />
    </div>
  );
}
