// components/thread.tsx
import React from 'react';
import '../styles/thread.css';

export interface Message {
  text: string;
  fromUser: boolean;
  threadId?: string; // Make sure types are consistent, changed from number to string
  isParent?: boolean;
}

export interface ThreadProps {
  parentMessage: Message;
  childMessages: Message[];
  isThreadActive: boolean;
  onClick: () => void;
}

const Thread: React.FC<ThreadProps> = ({ parentMessage, childMessages, isThreadActive, onClick }) => {
    // Determine if this message should have clickable behavior
    const isClickable = parentMessage.isParent && !parentMessage.fromUser;
    const messageBoxClass = `message-box ${isThreadActive ? 'message-box-selected' : ''} ${isClickable ? 'hoverable-clickable' : ''}`;

    return (
        <div className="all-messages">
            {/* Parent Message */}
            <div 
                className={messageBoxClass}
                onClick={() => isClickable && onClick()}
            >
                <span className="chat-text">
                    <strong>{parentMessage.fromUser ? 'User:' : 'Atlas:'}</strong> {parentMessage.text}
                </span>
            </div>

            {/* Child Messages */}
            {childMessages.length > 0 && (
                <div className="thread-children-container">
                    {childMessages.map((child, index) => (
                        <div 
                            className="message-box child-message" 
                            key={index}
                        >
                            <span className="chat-text">
                                <strong>{child.fromUser ? 'User:' : 'Atlas:'}</strong> {child.text}
                            </span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Thread;
