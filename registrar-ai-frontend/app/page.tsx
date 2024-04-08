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
    const [isProcessing, setIsProcessing] = useState<boolean>(false); // Add this line
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
            
            setIsProcessing(true); // Disable input field while processing
            try {
                const response = await fetch('https://atlas-backend-52c8a40a2751.herokuapp.com/process_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',  // This line is added to handle credentials like cookies
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
            setIsProcessing(false); // Re-enable input field after processing
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
        <div className="pane-container">
            <div className="welcome-text-container">
                <p className="welcome-text">Welcome to Duke Atlas, your tool to navigate your academic world.</p>
                <p className="welcome-text">Here are a few tips on how to use Atlas:</p>
                <ul className="welcome-text">
                    <li>To ask questions about courses, select &quot;Course Info&quot; above the chat field</li>
                    <li>To ask questions about registration, select &quot;Registration&quot; above the chat field</li>
                    <li>For other inquiries, select &quot;Other&quot; above the chat field</li>
                    <li>To reference a specific class, type the &quot;@&quot; sign followed by the class name (i.e. @AIPI 520). You can reference multiple classes in the same query.</li>
                    <li>To follow-up on an Atlas response, click on the message.</li>
                </ul>
            </div>
        </div>
        <div className="center-container">
            <div className="chat-interface-container">
                <div className="chat-window" ref={chatWindowRef}>
                    {messages
                        // Filter to get only parent messages based on 'isParent' property
                        .filter(msg => msg.isParent)
                        .map((parentMessage) => {
                            // Find child messages for each parent message based on 'threadId'
                            const childMessages = messages.filter(msg => msg.threadId === parentMessage.threadId && !msg.isParent);
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
                    {/* Loading indicator at the bottom of the chat */}
                    {isProcessing && (
                        <div className="loading-dots">
                            <strong className="loading-dots-text">Atlas:</strong>
                            <div className="dot"></div>
                            <div className="dot"></div>
                            <div className="dot"></div>
                        </div>
                    )}
                </div>
                <Input 
                    onSendMessage={handleSendMessage}
                    isFollowingUp={parentMessage !== undefined}
                    deselectMessage={deselectMessage}
                    isProcessing={isProcessing}
                />
            </div>
        </div>
        <div className="pane-container"></div>
    </div>
);
}

const Page: React.FC = () => { // Correctly annotated return type as React Functional Component
  return <ChatInterface />;
};

export default Page;
