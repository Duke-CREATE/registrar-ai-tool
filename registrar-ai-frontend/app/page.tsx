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
  onSelect: (text: string) => void; // Add this line
}
function Recommendation({ recommendation, onSelect }: RecommendationProps & { onSelect: (text: string) => void }) {
  return (
    <button className="recommendation-box" onClick={() => onSelect(recommendation)}>
      <p className="recommendation-text">{recommendation}</p>
    </button>
  );
}

// InputRecommendations
// Description: A field for displaying recommendations.
// Contains: 4 Recommendation
// Props: None
function InputRecommendations({ onSelect }: { onSelect: (text: string) => void }) {
  const recommendations = [
    "Courses that teach machine learning",
    "Courses about product management",
    "Fintech courses on Tuesdays and Thursdays",
    "Environmental engineering courses",
  ];

  return (
    <div className="input-recommendations">
      {recommendations.map((rec, index) => (
        <Recommendation key={index} recommendation={rec} onSelect={onSelect} />
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
  // messages initialized as an empty array
  const [messages, setMessages] = useState<string[]>([]);
  // inputRef initialized as a null reference
  const inputRef = useRef<HTMLInputElement>(null);

  // asynchronous function handleSendMessage
  // async keyword indicates that the function will preform asynchronous operations
  // uses the await keyword to wait for promises to resolve (fetch to complete)
  const handleSendMessage = async () => {
    if (inputRef.current && inputRef.current.value.trim() !== '') {
      const userMessage = inputRef.current.value;

      console.log('Sending message:', userMessage);
      
      // Clear the input field
      inputRef.current.value = '';

      // Update the local state to display the user message
      setMessages(prevMessages => [...prevMessages, `You: ${userMessage}`]);

      // Send the message to the backend
      try {
        const response = await fetch('http://127.0.0.1:5000/process_message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ user_message: userMessage }),
        });

        if (response.ok) {
          const responseData = await response.json();
          console.log('Response received:', responseData);

          // Check if responseData is not empty
          // and update the local state to display the backend response
          if (responseData.response) {
            setMessages(prevMessages => [...prevMessages, `Reply: ${responseData.response}`]);
          }
        } else {
          console.error('Failed to send message');
        }
      } catch (error) {
        console.error('Error sending message:', error);
      }
      } else {
      console.log('Input is empty or ref is not set');
      }
    };

  const handleRecommendationSelect = (text: string) => {
    setMessages(prevMessages => [...prevMessages, text]);
  };

  return (
    <div className="main-content">
      <div className="send-chat-field">
        <input type="text" className="chat-input" ref={inputRef} />
        <button className="chat-input-button" onClick={handleSendMessage}>
          Send
        </button>
      </div>
      <div>
        <InputRecommendations onSelect={handleRecommendationSelect} />
      </div>
      <div className="chat-window">
        {messages.map((message, index) => (
        <p className="chat-text" key={index}>{message}</p>
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
    <ChatInterface />
  );
}
