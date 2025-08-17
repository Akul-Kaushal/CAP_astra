import { Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatMessageProps {
  content: string;
  isUser: boolean;
  image?: string;
  timestamp?: Date;
}

const ChatMessage = ({ content, isUser, image, timestamp }: ChatMessageProps) => {
  return (
    <div className={cn("flex gap-3 mb-6 message-enter", isUser ? "flex-row-reverse" : "flex-row")}>
      {/* Avatar */}
      <div className={cn(
        "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
        isUser ? "bg-primary text-primary-foreground" : "bg-accent-muted text-accent-foreground"
      )}>
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>
      
      {/* Message content */}
      <div className={cn(
        "message-bubble",
        isUser ? "user-message" : "ai-message"
      )}>
        {image && (
          <div className="mb-3">
            <img 
              src={image} 
              alt="Uploaded content" 
              className="rounded-lg max-w-full h-auto shadow-sm"
              style={{ maxHeight: "300px" }}
            />
          </div>
        )}
        
        <p className="text-sm leading-relaxed whitespace-pre-wrap">{content}</p>
        
        {timestamp && (
          <div className={cn(
            "text-xs mt-2 opacity-60",
            isUser ? "text-right" : "text-left"
          )}>
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;