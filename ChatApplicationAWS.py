import asyncio
import websockets
import json
import tkinter as tk
from tkinter import scrolledtext
import threading

# AWS WebSocket API URL (Replace with your WebSocket API Gateway URL)
WEBSOCKET_URL = "wss://qke9fyw7si.execute-api.ap-south-1.amazonaws.com/production/"

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AWS WebSocket Chat")
        self.root.geometry("500x400")

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=15)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Message input field
        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.pack(padx=10, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.on_send_click)
        self.send_button.pack(padx=10, pady=5, side=tk.RIGHT)

        # WebSocket connection
        self.websocket = None

        # Start asyncio event loop in a separate thread
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.run_event_loop, daemon=True).start()

        # Connect to WebSocket
        self.loop.call_soon_threadsafe(asyncio.create_task, self.connect())

    def run_event_loop(self):
        """Runs the asyncio event loop in a separate thread."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def connect(self):
        """Connects to AWS WebSocket API."""
        try:
            self.websocket = await websockets.connect(WEBSOCKET_URL)
            self.append_message("? Connected to WebSocket Server")
            asyncio.create_task(self.receive_messages())  # Start receiving messages
        except Exception as e:
            self.append_message(f"? Connection Failed: {e}")

    async def receive_messages(self):
        """Receives messages from WebSocket server."""
        while True:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                self.append_message(f"? {data['message']}")
            except websockets.exceptions.ConnectionClosed:
                self.append_message("? Disconnected. Reconnecting...")
                self.loop.call_soon_threadsafe(asyncio.create_task, self.connect())
                break

    async def send_message(self, message):
        """Sends message to WebSocket API."""
        if message and self.websocket:
            await self.websocket.send(json.dumps({"action": "sendmessage", "message": message}))
            self.append_message(f"? You: {message}")

    def on_send_click(self):
        """Handles Send button click."""
        message = self.message_entry.get().strip()
        if message:
            self.message_entry.delete(0, tk.END)
            self.loop.call_soon_threadsafe(asyncio.create_task, self.send_message(message))  # Runs properly now

    def append_message(self, message):
        """Appends a message to the chat display (Tkinter thread-safe)."""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

# Run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
