import { useNavigate } from "react-router-dom";
import { Bot, Sparkles, ArrowRight, MessageCircle, Zap, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center space-y-8 max-w-4xl mx-auto">
          {/* Logo and Title */}
          <div className="flex items-center justify-center space-x-4 mb-12">
            <div className="relative">
              <Bot size={64} className="text-primary" />
              <Sparkles size={24} className="absolute -top-2 -right-2 text-accent" />
            </div>
            <div>
              <h1 className="text-5xl lg:text-7xl font-bold text-foreground">ASTRA</h1>
              <p className="text-xl text-accent font-medium">Your Intelligent Companion</p>
            </div>
          </div>
          
          {/* Main Headline */}
          <div className="space-y-6">
            <h2 className="text-3xl lg:text-4xl font-semibold text-foreground leading-tight">
              Experience the Future of AI Conversation
            </h2>
            <p className="text-xl text-accent leading-relaxed max-w-2xl mx-auto">
              Get instant answers, creative assistance, and intelligent insights. 
              ASTRA is here to help you with any question, anytime.
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-12">
            <Button 
              size="lg" 
              className="text-lg px-8 py-6"
              onClick={() => navigate('/login')}
            >
              Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button 
              variant="secondary" 
              size="lg" 
              className="text-lg px-8 py-6"
              onClick={() => navigate('/login')}
            >
              Sign In
            </Button>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-24">
          <h3 className="text-2xl font-semibold text-foreground text-center mb-12">
            Why Choose ASTRA?
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <Card className="text-center p-6 hover:shadow-lg transition-shadow">
              <CardContent className="pt-6">
                <MessageCircle className="h-12 w-12 text-primary mx-auto mb-4" />
                <h4 className="font-semibold text-foreground mb-3 text-lg">Smart Conversations</h4>
                <p className="text-accent">Engage in natural, intelligent conversations that understand context and nuance</p>
              </CardContent>
            </Card>
            
            <Card className="text-center p-6 hover:shadow-lg transition-shadow">
              <CardContent className="pt-6">
                <Zap className="h-12 w-12 text-primary mx-auto mb-4" />
                <h4 className="font-semibold text-foreground mb-3 text-lg">Lightning Fast</h4>
                <p className="text-accent">Get instant responses with cutting-edge AI technology that thinks at the speed of thought</p>
              </CardContent>
            </Card>
            
            <Card className="text-center p-6 hover:shadow-lg transition-shadow">
              <CardContent className="pt-6">
                <Shield className="h-12 w-12 text-primary mx-auto mb-4" />
                <h4 className="font-semibold text-foreground mb-3 text-lg">Always Available</h4>
                <p className="text-accent">24/7 availability means ASTRA is ready to help whenever inspiration strikes</p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-24">
          <div className="bg-card/50 rounded-2xl p-8 max-w-2xl mx-auto">
            <h3 className="text-2xl font-semibold text-foreground mb-4">
              Ready to start your AI journey?
            </h3>
            <p className="text-accent mb-6">
              Join thousands of users who are already experiencing the power of ASTRA
            </p>
            <Button 
              size="lg"
              className="text-lg px-8 py-6"
              onClick={() => navigate('/login')}
            >
              Start Chatting Now
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;