import ChatHeader from "@/components/ChatHeader";
import ChatInterface from "@/components/ChatInterface";

const Chat = () => {
  return (
    <div className="h-screen flex flex-col bg-chat-background">
      <ChatHeader />
      <ChatInterface />
    </div>
  );
};

export default Chat;