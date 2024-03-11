// app/page.tsx
'use client';
import React, { useState, useEffect } from 'react';
import Input from './components/input';
import Thread from './components/thread';
import './styles/page.css';

interface Message {
  text: string;
  fromUser: boolean;
  threadId?: string;
  isParent?: boolean; // This doesn't seem to be set in your current logic but conceptual for sorting
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [selectedMessageIndex, setSelectedMessageIndex] = useState<number | null>(null);

  const isFollowingUp = selectedMessageIndex !== null;

  const handleSendMessage = async (userMessage: string, tags: string[], queryType: string) => {
      let threadId: string | undefined = "";
      let isParent: boolean = true;

      if (isFollowingUp) {
          const parentMessage = messages[selectedMessageIndex!];
          threadId = parentMessage.threadId;
          isParent = false;
      }

      if (userMessage.trim() !== '') {
          const newMessage: Message = {
              text: userMessage,
              fromUser: true,
              threadId,
              isParent,
          };
          setMessages(prevMessages => [...prevMessages, newMessage]);

          const payload = {
              user_message: userMessage,
              tags: tags,
              query_type: queryType,
              conversation_history: isFollowingUp ? messages.filter(msg => msg.threadId === threadId) : [],
              threadId: threadId,
          };

          try {
              const response = await fetch('http://127.0.0.1:5000/process_message', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify(payload),
              });

              if (response.ok) {
                  const responseData = await response.json();
                  const responseMessage: Message = {
                      text: responseData.response,
                      fromUser: false,
                      threadId: responseData.threadId,
                  };
                  setMessages(prevMessages => [...prevMessages, responseMessage]);
              } else {
                  console.error('Failed to send message');
              }
          } catch (error) {
              console.error('Error sending message:', error);
          }
      }
  };

  const deselectMessage = () => {
      setSelectedMessageIndex(null);
  };

  const handleThreadClick = (index: number) => {
      setSelectedMessageIndex(prevIndex => prevIndex === index ? null : index);
  };

  useEffect(() => {
      const savedMessages = sessionStorage.getItem('conversation_history');
      if (savedMessages) {
          setMessages(JSON.parse(savedMessages));
      }
  }, []);

  return (
    <div className="main-content">
      <div className="welcome-text-container">
        <p className="welcome-text">
          Welcome to Duke Atlas, your tool to navigate your academic world.
          To reference a specific class, type the @ sign followed by the class name (i.e. @AIPI 520).
          You can reference multiple classes in the same query.
        </p>
      </div>
      <div className="chat-window">
                {messages.filter((msg, index, array) => array.findIndex(m => m.threadId === msg.threadId) === index)
                .map((parentMessage, index) => {
                    const childMessages = messages.filter(msg => msg.threadId === parentMessage.threadId && msg.isParent !== true);
                    return (
                        <Thread 
                            key={index} 
                            parentMessage={parentMessage} 
                            childMessages={childMessages} 
                            onClick={() => handleThreadClick(index)} 
                            isThreadActive={selectedMessageIndex === index}
                        />
                    );
                })}
            </div>
            <Input 
                onSendMessage={handleSendMessage}
                isFollowingUp={isFollowingUp}
                deselectMessage={deselectMessage}
            />
        </div>
  );
}

const Page: React.FC = () => { // Correctly annotated return type as React Functional Component
  return <ChatInterface />;
};

export default Page; // Ensure this is correct
