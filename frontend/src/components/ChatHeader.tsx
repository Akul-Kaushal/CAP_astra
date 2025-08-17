import { Bot, Sparkles } from "lucide-react";

const ChatHeader = () => {
  return (
    <header className="header-gradient text-white sticky top-0 z-50 shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-center space-x-3">
          <div className="relative">
            <Bot size={32} className="text-white" />
            <Sparkles size={16} className="absolute -top-1 -right-1 text-yellow-300" />
          </div>
          <div className="text-center">
            <h1 className="text-2xl font-bold">ASTRA</h1>
            <p className="text-sm opacity-90">Your intelligent companion for any question</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default ChatHeader;