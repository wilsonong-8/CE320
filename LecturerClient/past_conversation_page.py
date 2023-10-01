import tkinter as tk
from tkinter import scrolledtext


class PastConversation(tk.Toplevel):
    def __init__(self, parent, conversation):
        super().__init__(parent, bg="#fae0e4")
        self.title("Conversation History")
        self.parent = parent
        self.conversation = conversation

        window_width = 450
        window_height = 250

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window size and position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        chat_history_label = tk.Label(self, text="Chat History:", font=("Arial", 15), bg="#fae0e4")
        chat_history_label.pack()

        # Extract messages from the conversation and join them as a string
        messages = "\n".join(message.strip() for message in conversation)

        self.message_history = scrolledtext.ScrolledText(self, wrap="word", width=68, height=10)
        self.message_history.insert(tk.END, messages)
        self.message_history.pack()
        self.message_history.config(state="disabled")

        send_button = tk.Button(self, text="Close", command=self.close_window)
        send_button.pack(side=tk.BOTTOM)

    def close_window(self):
        self.destroy()
