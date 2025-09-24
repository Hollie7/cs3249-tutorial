import { useState } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const BACKEND_URL = "http://localhost:8001/chat"; // adjust if needed

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);

    try {
      const resp = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await resp.json();
      const reply = data.response || "[No response]";
      setMessages([...newMessages, { role: "assistant", content: reply }]);
    } catch (err) {
      setMessages([
        ...newMessages,
        { role: "assistant", content: "[Error contacting backend]" },
      ]);
    }

    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div
      style={{
        maxWidth: "600px",
        margin: "2rem auto",
        fontFamily: "sans-serif",
      }}
    >
      <h2>💬 CS3249 Minimal CUI (React + TS)</h2>

      <div
        style={{
          border: "1px solid #ccc",
          padding: "1rem",
          borderRadius: "8px",
          height: "400px",
          overflowY: "auto",
        }}
      >
        {messages.map((msg, idx) => (
          <div key={idx} style={{ marginBottom: "0.5rem" }}>
            <strong>{msg.role === "user" ? "You" : "Bot"}:</strong>{" "}
            {msg.content}
          </div>
        ))}
      </div>

      <div style={{ marginTop: "1rem", display: "flex" }}>
        <textarea
          rows={2}
          style={{ flex: 1, marginRight: "0.5rem" }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
