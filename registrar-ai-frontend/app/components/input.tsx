import React, { useState, useEffect, useRef } from 'react';
import '../styles/input.css';

interface InputProps {
  onSendMessage: (message: string, tags: string[]) => void; // callback to send message
}

const Input: React.FC<InputProps> = ({ onSendMessage }) => {
  const [inputContent, setInputContent] = useState('');
  const [isTagging, setIsTagging] = useState(false);
  const [classes, setClasses] = useState<string[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const editableRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch('classes.json') // Adjust the path as needed
      .then((response) => response.json())
      .then((data: string[]) => setClasses(data));
  }, []);

  useEffect(() => {
    if (isTagging) {
      // Attempt to get the current word being typed, ensure it defaults to an empty string if undefined
      const words = inputContent.split(' ');
      const query = words.pop() || ''; // Ensure query is never undefined

      if (query.startsWith('@')) {
        const searchTerm = query.substring(1).toLowerCase(); // Remove '@' and convert to lower case for matching
        const filteredClasses = classes.filter(cls => cls.toLowerCase().startsWith(searchTerm));
        setSuggestions(filteredClasses);
      } else {
        setIsTagging(false);
        setSuggestions([]);
      }
    }
  }, [inputContent, isTagging, classes]);

  const handleInput = (e: React.FormEvent<HTMLDivElement>) => {
    const text = e.currentTarget.innerText;
    setInputContent(text);
    // Check if the user is typing a tag (indicated by '@')
    setIsTagging(text.includes('@'));
  };

  const selectSuggestion = (suggestion: string) => {
    if (!editableRef.current) return;
  
    setIsTagging(false);
    setSuggestions([]);
  
    // Find the last '@' and the partial text to replace
    const currentHtml = editableRef.current.innerHTML;
    const lastAtIndex = currentHtml.lastIndexOf('@');
    if (lastAtIndex !== -1) {
      // Generate the non-editable tag HTML without the '@'
      const tagHtml = `<span class="tag" contenteditable="false">${suggestion}</span>&nbsp;`;
  
      // Replace from last '@' to the end of the string with the full tag HTML
      const newHtml = currentHtml.substring(0, lastAtIndex) + tagHtml + currentHtml.substring(lastAtIndex + suggestion.length + 1);
      editableRef.current.innerHTML = newHtml;
    }
  
    // Focus back on the contentEditable element and move the cursor to the end
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

  return (
    <div className="chat-input-container">
      <div
        ref={editableRef}
        contentEditable
        className="chat-input-content"
        onInput={handleInput}
        data-placeholder="Type here..."
      ></div>
      {isTagging && suggestions.length > 0 && (
        <div className="tagging-suggestions">
          {suggestions.map((suggestion, index) => (
            <div key={index} onClick={() => selectSuggestion(suggestion)} className="tagging-option">
              {suggestion}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Input;


