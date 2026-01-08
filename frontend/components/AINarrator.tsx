import React, { useState, useEffect } from 'react';

interface AINarratorProps {
  message: string;
}

const AINarrator: React.FC<AINarratorProps> = ({ message }) => {
  const [isVisible, setIsVisible] = useState(true);
  const [showSpeechBubble, setShowSpeechBubble] = useState(false);

  // Show speech bubble when message changes
  useEffect(() => {
    setShowSpeechBubble(true);
    const timer = setTimeout(() => {
      setShowSpeechBubble(false);
    }, 5000); // Hide after 5 seconds

    return () => clearTimeout(timer);
  }, [message]);

  return (
    <div className={`fixed bottom-6 right-6 z-50 transition-all duration-300 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
      {/* Narrator character */}
      <div
        className="relative cursor-pointer"
        onClick={() => setShowSpeechBubble(!showSpeechBubble)}
      >
        <div className="w-16 h-16 bg-gradient-to-b from-purple-700 to-purple-900 rounded-full flex items-center justify-center border-4 border-yellow-500 shadow-lg">
          <span className="text-3xl">🧙‍♂️</span>
        </div>

        {/* Speech bubble */}
        {showSpeechBubble && (
          <div className="absolute bottom-full mb-2 right-0 w-64 comic-speech transform origin-bottom-right animate-fadeIn">
            <p className="text-sm font-medium">{message}</p>
          </div>
        )}
      </div>

      {/* Toggle button */}
      <button
        className="mt-2 w-full rpg-button text-xs py-1 rounded"
        onClick={() => setIsVisible(!isVisible)}
      >
        {isVisible ? 'Hide' : 'Show'} Narrator
      </button>
    </div>
  );
};

export default AINarrator;