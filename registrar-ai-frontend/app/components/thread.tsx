// components/thread.tsx
import React from 'react';
import '../styles/thread.css';

export interface Message {
  text: string;
  fromUser: boolean;
  threadId?: string; // Make sure types are consistent, changed from number to string
}

export interface ThreadProps {
  parentMessage: Message;
  childMessages: Message[];
  isThreadActive: boolean;
  onClick: () => void;
}

const Thread: React.FC<ThreadProps> = ({ parentMessage, childMessages, isThreadActive, onClick }) => {
  return (
      <div className="all-messages">
          <div 
              className={`message-box ${isThreadActive ? 'message-box-selected' : ''}`} 
              onClick={onClick}
          >
              <span className="chat-text">
                  <strong>{parentMessage.fromUser ? 'User:' : 'Atlas:'}</strong> {parentMessage.text}
              </span>
          </div>
          {childMessages.map((child, index) => (
              <div 
                  className="message-box child-message" 
                  key={index}
                  style={{ marginLeft: '20px' }}
              >
                  <span className="chat-text">
                      <strong>{child.fromUser ? 'User:' : 'Atlas:'}</strong> {child.text}
                  </span>
              </div>
          ))}
      </div>
  );
};

export default Thread;
