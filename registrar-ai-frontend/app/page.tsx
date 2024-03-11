// app/page.tsx
'use client';
import React, { useState, useEffect, useRef } from 'react';
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
    // selectedMessageIndex is the index of the message that is currently selected
    const [selectedThreadId, setSelectedThreadId] = useState<string | null>(null);
    const parentMessage = messages.find(msg => msg.threadId === selectedThreadId);
    const chatWindowRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (chatWindowRef.current) {
            const { scrollHeight, clientHeight } = chatWindowRef.current;
            chatWindowRef.current.scrollTo(0, scrollHeight - clientHeight);
        }
    }, [messages]); // Dependency array ensures this runs only when messages change
    

    const handleSendMessage = async (userMessage: string, tags: string[], queryType: string) => {
        let threadId: string | undefined = "";
        let isParent: boolean = true;

        if (parentMessage) {
            threadId = parentMessage.threadId;
            isParent = false;
        }        
        // if userMessage is not empty, create a new message and add it to the messages state
        if (userMessage.trim() !== '') {
            const newMessage: Message = {
                text: userMessage,
                fromUser: true,
                threadId,
                isParent,
            };
            // add new message to the messages state
            setMessages(prevMessages => [...prevMessages, newMessage]);

            
            const payload = {
                user_message: userMessage,
                tags: tags,
                query_type: queryType,
                conversation_history: parentMessage ? messages.filter(msg => msg.threadId === threadId) : [],
                threadId: threadId || '',
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
                        isParent: responseData.isParent,
                        threadId: responseData.threadId
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
    setSelectedThreadId(null);
};

const handleThreadClick = (threadId: string) => {
    setSelectedThreadId(prevThreadId => prevThreadId === threadId ? null : threadId);
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
        <div className="chat-window" ref={chatWindowRef}>
            {messages
                // Filter to get only parent messages based on 'isParent' property
                .filter(msg => msg.isParent)
                .map((parentMessage, index) => {
                    // Find child messages for each parent message based on 'threadId'
                    const childMessages = messages.filter(msg => msg.threadId === parentMessage.threadId && !msg.isParent);
                    console.log('Parent message:', parentMessage);
                    console.log('Child messages:', childMessages);
                    return (
                        <Thread 
                            key={parentMessage.threadId} 
                            parentMessage={parentMessage} 
                            childMessages={childMessages} 
                            onClick={() => handleThreadClick(parentMessage.threadId || '')} 
                            isThreadActive={selectedThreadId === parentMessage.threadId}
                        />
                    );
                })}
        </div>
        <Input 
            onSendMessage={handleSendMessage}
            isFollowingUp={parentMessage !== undefined}
            deselectMessage={deselectMessage}
        />
        </div>
  );
}

const Page: React.FC = () => { // Correctly annotated return type as React Functional Component
  return <ChatInterface />;
};

export default Page;
