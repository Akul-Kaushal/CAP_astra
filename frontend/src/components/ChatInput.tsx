import { useState, useRef } from "react";
import { Send, ImagePlus, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "@/hooks/use-toast";

interface ChatInputProps {
  onSendMessage: (message: string, image?: File) => void;
  disabled?: boolean;
}

const ChatInput = ({ onSendMessage, disabled }: ChatInputProps) => {
  const [message, setMessage] = useState("");
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        toast({
          title: "Image too large",
          description: "Please select an image smaller than 10MB.",
          variant: "destructive",
        });
        return;
      }

      if (!file.type.startsWith('image/')) {
        toast({
          title: "Invalid file type",
          description: "Please select an image file.",
          variant: "destructive",
        });
        return;
      }

      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemoveImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSend = () => {
    if (message.trim() || selectedImage) {
      onSendMessage(message.trim(), selectedImage || undefined);
      setMessage("");
      setSelectedImage(null);
      setImagePreview(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="sticky bottom-0 bg-background/80 backdrop-blur-sm border-t border-border p-4">
      <div className="container mx-auto max-w-4xl">
        {/* Image preview */}
        {imagePreview && (
          <div className="mb-4 relative inline-block">
            <img 
              src={imagePreview} 
              alt="Preview" 
              className="h-20 w-20 object-cover rounded-lg shadow-md"
            />
            <Button
              size="sm"
              variant="destructive"
              className="absolute -top-2 -right-2 h-6 w-6 rounded-full p-0"
              onClick={handleRemoveImage}
            >
              <X size={12} />
            </Button>
          </div>
        )}
        
        <div className="flex items-end gap-3">
          {/* Image upload button */}
          <Button
            type="button"
            variant="secondary"
            size="sm"
            className="upload-button flex-shrink-0"
            onClick={() => fileInputRef.current?.click()}
            disabled={disabled}
          >
            <ImagePlus size={18} />
            <span className="sr-only">Upload image</span>
          </Button>
          
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageSelect}
            className="hidden"
          />
          
          {/* Message input */}
          <div className="flex-1 relative">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask ASTRA anything or upload an image..."
              className="chat-input w-full resize-none min-h-[52px] max-h-32"
              rows={1}
              disabled={disabled}
            />
          </div>
          
          {/* Send button */}
          <Button
            onClick={handleSend}
            disabled={disabled || (!message.trim() && !selectedImage)}
            className="send-button flex-shrink-0"
          >
            <Send size={18} />
            <span className="sr-only">Send message</span>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;