// app/page.tsx
'use client';
import React, { useRef, useState, useEffect } from 'react';
import Input from './components/input';
import './styles/page.css';

// ===============
// =============== CHAT INTERFACE ===============
// ===============

// ChatWindow
// Description: Where user's sent input and system responses are displayed.
// Contains: None
// Props: None
function ChatInterface() {
  // messages initialized as an empty array
  const [messages, setMessages] = useState<{ text: string; fromUser: boolean }[]>([]);

  // asynchronous function handleSendMessage
  // async keyword indicates that the function will preform asynchronous operations
  // uses the await keyword to wait for promises to resolve (fetch to complete)
  const handleSendMessage = async (userMessage: string, tags: string[]) => {
    if (userMessage.trim() !== '') {
      // Update messages state to include the new user message
      setMessages(prevMessages => [...prevMessages, { text: userMessage, fromUser: true }]);
  
      // Since state updates are asynchronous, use the updated state for further logic
      // Here, we directly proceed with sending the message without waiting for the state to update
      // and construct what the current conversation would be after the update.
      const currentConversation = [...messages, { text: userMessage, fromUser: true }];
  
      try {
        const response = await fetch('http://127.0.0.1:5000/process_message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_message: userMessage,
            tags: tags,
            conversation_history: currentConversation,
          }),
        });
  
        if (response.ok) {
          const responseData = await response.json();
          if (responseData.response) {
            setMessages(prevMessages => [...prevMessages, { text: responseData.response, fromUser: false }]);
            // Note: Storing the entire conversation in session storage might not be the best approach
            // Consider storing only necessary identifiers or state markers
          }
        } else {
          console.error('Failed to send message');
        }
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };  

  useEffect(() => {
    const savedMessages = sessionStorage.getItem('conversation_history');
    if (savedMessages) {
      setMessages(JSON.parse(savedMessages));
    }
  }, []);

  return (
    <div className="main-content">
      <p className="welcome-text">
        Welcome to Duke Atlas, your tool to naviagte your academic world.
        To reference a specific class, type the @ sign followed by the class name (i.e. @AIPI 520). You can reference multiple classes in the same query.</p>
        <Input onSendMessage={handleSendMessage} />
      <div className="chat-window">
        {messages.map((message, index) => (
          <p className="chat-text" key={index}>
            <span style={{fontWeight: 'bold'}}>
              {message.fromUser ? 'User' : 'Atlas'}:
            </span>{' '}
            {message.text}
          </p>
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
