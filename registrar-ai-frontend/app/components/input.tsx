// components/input.tsx
import React, { useState, useEffect, useRef } from 'react';
import '../styles/input.css';

interface InputProps {
  onSendMessage: (message: string, tags: string[], queryType: string) => void;
  isFollowingUp: boolean;
  deselectMessage: () => void;
}

const Input: React.FC<InputProps> = ({ onSendMessage, isFollowingUp, deselectMessage }) => {
  const [inputContent, setInputContent] = useState('');
  const [isTagging, setIsTagging] = useState(false);
  const [classes, setClasses] = useState<string[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [queryType, setQueryType] = useState('Class Info'); // Added state for selected query type
  const editableRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch('classes.json')
      .then((response) => response.json())
      .then((data: string[]) => setClasses(data));
  }, []);

  useEffect(() => {
    if (isTagging) {
      const words = inputContent.split(' ');
      const query = words.pop() || '';
      if (query.startsWith('@')) {
        const searchTerm = query.substring(1).toLowerCase();
        const filteredClasses = classes.filter(cls => cls.toLowerCase().startsWith(searchTerm));
        setSuggestions(filteredClasses);
      } else {
        setIsTagging(false);
        setSuggestions([]);
      }
    }
  }, [inputContent, isTagging, classes]);

  useEffect(() => {
    console.log('Input component isFollowingUp:', isFollowingUp);
  }, [isFollowingUp]);

  const handleInput = (e: React.FormEvent<HTMLDivElement>) => {
    const text = e.currentTarget.innerText;
    setInputContent(text);
    setIsTagging(text.includes('@'));
  };

  const selectSuggestion = (suggestion: string) => {
    // Directly return if editableRef.current is null to avoid any null-related errors
    if (!editableRef.current) return;

    setIsTagging(false);
    setSuggestions([]);

    // Now we know for sure editableRef.current is not null, so we can safely access its properties
    const currentHtml = editableRef.current.innerHTML; // innerHTML is always a string, so it's safe
    const lastAtIndex = currentHtml.lastIndexOf('@');
    if (lastAtIndex !== -1) {
      const beforeAt = currentHtml.substring(0, lastAtIndex);
      const afterAt = currentHtml.substring(lastAtIndex).split(' ')[0]; // This might be the problematic part if using textContent
      const remainingText = currentHtml.substring(lastAtIndex + afterAt.length);
      const tagHtml = `<span class="tag" contenteditable="false">${suggestion}</span>&nbsp;`;
      editableRef.current.innerHTML = beforeAt + tagHtml + remainingText;
    }

    moveCursorToEnd();
};

  const moveCursorToEnd = () => {
    if (!editableRef.current) return;
    editableRef.current.focus();
    const range = document.createRange();
    const sel = window.getSelection();
    if (sel && editableRef.current.lastChild) {
      range.setStartAfter(editableRef.current.lastChild);
      range.collapse(true);
      sel.removeAllRanges();
      sel.addRange(range);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Backspace' && isFollowingUp && editableRef.current?.innerText === '') {
      deselectMessage();
    }
  };

  const onSubmit = () => {
    if (!editableRef.current) return;

    const tags: string[] = [];
    const tagElements = editableRef.current.querySelectorAll('.tag');
    tagElements.forEach(tag => {
        const tagText = tag.textContent;
        if (tagText) tags.push(tagText);
    });

    let messageContent = editableRef.current.innerText.trim();
    if (messageContent) {
        onSendMessage(messageContent, tags, queryType);

        // Resetting the input area and deselecting the message after sending
        editableRef.current.innerHTML = '';
        setInputContent('');
        deselectMessage();  // Ensure this is called to reset following up state in the parent component
    }
};

  return (
    <div className='input-container'>
      <div className="query-type-buttons-container">
        <p className="query-type-text">What would you like to know about?</p>
        {['Class Info', 'Registration', 'Other'].map((type) => ( // Changed queryType to type
          <button
            key={type}
            className={`query-type-button ${queryType === type ? 'active' : ''}`} // Changed queryType to type for comparison
            onClick={() => setQueryType(type)} // Changed queryType to type
          >
            {type}
          </button>
        ))}
      </div>
      <div className="chat-input-container">
      <div className="chat-field">
        <div className='thread-icon-container'>
            {isFollowingUp &&
            (<img src="thread-rep.svg" alt="Follow-up in thread" className="follow-up-icon" style={{ display: isFollowingUp ? 'inline' : 'none' }}/>)
            }
        </div>
        <div
          ref={editableRef}
          contentEditable
          className="chat-input-content"
          onInput={handleInput}
          onKeyDown={handleKeyDown}
          data-placeholder={isFollowingUp ? "Follow-up in thread" : "Ask Duke Atlas..."}
        >
        </div>
      </div>
        {isTagging && suggestions.length > 0 && (
          <div className="tagging-suggestions">
            {suggestions.map((suggestion, index) => (
              <div key={index} className="tagging-option" onClick={() => selectSuggestion(suggestion)}>
                {suggestion}
              </div>
            ))}
          </div>
        )}
        <button className="send-chat-button" onClick={onSubmit}>Submit</button>
      </div>
    </div>
  );
};

export default Input;
