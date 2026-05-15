import React, { useState, useEffect, useRef } from 'react';
import { Send, User, Bot, Paperclip, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsStreaming(true);

    try {
      // Mocking SSE for now - in Phase 5 real SSE will be added
      const responseMessage: Message = { role: 'assistant', content: '' };
      setMessages(prev => [...prev, responseMessage]);

      const mockResponse = "I am the IndiGo Operations Copilot. How can I help you today with your flight operations or SOP queries?";
      let currentContent = "";
      
      for (const char of mockResponse) {
        await new Promise(r => setTimeout(r, 20));
        currentContent += char;
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1].content = currentContent;
          return newMessages;
        });
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto bg-slate-900 shadow-2xl rounded-2xl overflow-hidden border border-slate-800">
      <div className="bg-indigo-900/50 p-4 border-b border-indigo-500/20 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Bot size={24} className="text-white" />
          </div>
          <div>
            <h2 className="font-bold text-white tracking-tight">Ops Copilot</h2>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Aviation Intelligence Active</span>
            </div>
          </div>
        </div>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
        <AnimatePresence initial={false}>
          {messages.map((msg, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  msg.role === 'user' ? 'bg-indigo-500' : 'bg-slate-700'
                }`}>
                  {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                </div>
                <div className={`p-4 rounded-2xl shadow-sm ${
                  msg.role === 'user' 
                    ? 'bg-indigo-600 text-white rounded-tr-none' 
                    : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-tl-none'
                }`}>
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        {isStreaming && messages[messages.length-1]?.content === '' && (
          <div className="flex justify-start">
             <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                  <Bot size={16} />
                </div>
                <div className="bg-slate-800 p-4 rounded-2xl rounded-tl-none border border-slate-700">
                  <Loader2 className="animate-spin text-indigo-400" size={18} />
                </div>
             </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-slate-900 border-t border-slate-800">
        <div className="relative flex items-center">
          <button className="absolute left-3 text-slate-500 hover:text-indigo-400 transition-colors">
            <Paperclip size={20} />
          </button>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask about flight SOPs, baggage ops, or crew policy..."
            className="w-full bg-slate-800 text-slate-200 pl-11 pr-14 py-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 border border-slate-700 placeholder:text-slate-500 transition-all"
          />
          <button
            onClick={handleSendMessage}
            className="absolute right-2 p-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-all shadow-lg active:scale-95"
          >
            <Send size={20} />
          </button>
        </div>
        <p className="text-[10px] text-center mt-3 text-slate-600 font-medium uppercase tracking-[0.1em]">
          Powered by Enterprise AI Operations Platform • Internal Use Only
        </p>
      </div>
    </div>
  );
};
