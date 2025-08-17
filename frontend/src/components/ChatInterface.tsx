import { useState, useRef, useEffect } from "react";
import { Loader2 } from "lucide-react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  image?: string;
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "Hello! I'm Aura AI, your intelligent assistant. I can help answer questions, analyze images, and assist with various tasks. How can I help you today?",
      isUser: false,
      timestamp: new Date(),
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateAIResponse = async (userMessage: string, hasImage: boolean): Promise<string> => {
    // Simulate AI response delay
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    const responses = hasImage ? [
      "I can see the image you've shared! It's quite interesting. Let me analyze what I see and provide some insights about it.",
      "Thanks for sharing that image! I can observe several details that might be relevant to your question. What would you like to know about it?",
      "That's a fascinating image! I can see various elements that I'd be happy to discuss with you. What specific aspects would you like me to focus on?",
      "I've analyzed your image and can provide detailed observations about what I see. Feel free to ask me anything specific about it!"
    ] : [
      "That's a great question! Let me think about that and provide you with a helpful response.",
      "I understand what you're asking. Here's my take on that topic based on what I know.",
      "Interesting! I can definitely help you with that. Let me break this down for you.",
      "Thanks for asking! I'll do my best to provide you with accurate and useful information about this.",
      "That's something I can help explain. Let me give you a comprehensive answer."
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleSendMessage = async (content: string, image?: File) => {
    if (!content && !image) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: content || "📷 Image shared",
      isUser: true,
      timestamp: new Date(),
      image: image ? URL.createObjectURL(image) : undefined,
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Generate AI response
      const aiResponse = await generateAIResponse(content, !!image);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: aiResponse,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error generating response:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I apologize, but I'm having trouble processing your request right now. Please try again in a moment.",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Chat messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="container mx-auto max-w-4xl">
          {messages.map((message) => (
            <ChatMessage
              key={message.id}
              content={message.content}
              isUser={message.isUser}
              image={message.image}
              timestamp={message.timestamp}
            />
          ))}
          
          {isLoading && (
            <div className="flex gap-3 mb-6">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-accent-muted flex items-center justify-center">
                <Loader2 size={16} className="animate-spin text-accent-foreground" />
              </div>
              <div className="ai-message message-bubble">
                <div className="flex items-center gap-2">
                  <Loader2 size={16} className="animate-spin" />
                  <span className="text-sm">Thinking...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Chat input */}
      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
};

export default ChatInterface;