"use client";

import { useState } from "react";
import Sidebar from "@/components/app-sidebar";

export default function Home() {
  const [messages, setMessages] = useState<{ text: string; sender: "user" | "bot" }[]>([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    setTimeout(() => {
      setMessages((prev) => [...prev, { text: "Hello! How can I assist you?", sender: "bot" }]);
    }, 1000);
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col p-6 bg-gray-100">
        <h1 className="text-2xl font-semibold mb-4">Aura AI</h1>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto bg-white p-4 rounded-lg shadow">
          {messages.map((msg, index) => (
            <div key={index} className={`mb-2 p-2 rounded-lg ${msg.sender === "user" ? "bg-blue-500 text-white self-end" : "bg-gray-200 text-gray-900 self-start"}`}>
              {msg.text}
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div className="flex items-center mt-4 p-2 bg-white rounded-lg shadow">
          <input
            type="text"
            className="flex-1 p-2 border rounded-lg outline-none"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button className="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg" onClick={handleSend}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
