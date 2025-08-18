import { useState, useRef, useEffect } from "react";
import { Loader2 } from "lucide-react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import { supabase } from "../lib/supabase"; 
import { askImage, askText } from "../lib/api"; 

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
      id: "1",
      content:
        "Hello! I'm Aura AI, your intelligent assistant. I can help answer questions, analyze images, and assist with various tasks. How can I help you today?",
      isUser: false,
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

const handleSendMessage = async (content: string, image?: File) => {

  
    if (!content && !image) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: content || " ",
      isUser: true,
      timestamp: new Date(),
      image: image ? URL.createObjectURL(image) : undefined,
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {

      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (!user) throw new Error("User not authenticated");

      let aiResponse;

    if (image) {
      aiResponse = await askImage({
        uid: user.id,
        prompt: content || "", 
        image,
      });
      const { task_recommendation, task_details, safety_specifications } = aiResponse;
      const combinedReply = `
      Task Recommendation: ${task_recommendation}

      Task Details:
      Confirmation: ${task_details.confirmation}
      Possible Actions:
      - ${task_details.possible_actions.join("\n- ")}
      Steps to Perform:
      - ${task_details.steps_to_perform.join("\n- ")}

      Safety Specifications:
      ${safety_specifications}
        `.trim();

        aiResponse.reply = combinedReply; 

    } else {
      aiResponse = await askText({
        uid: user.id,
        request: content!,
      });
    }

    const aiMessage: Message = {
      id: (Date.now() + 1).toString(),
      content: aiResponse.reply,
      isUser: false,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, aiMessage]);
  } catch (error) {
    console.error("Error generating response:", error);
    const errorMessage: Message = {
      id: (Date.now() + 1).toString(),
      content:
        "I’m having trouble processing your request right now. Please try again in a moment.",
      isUser: false,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, errorMessage]);
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
                <Loader2
                  size={16}
                  className="animate-spin text-accent-foreground"
                />
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
