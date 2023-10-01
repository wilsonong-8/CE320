import tkinter as tk
from tkinter import scrolledtext


class LecturerChat(tk.Toplevel):
    def __init__(self, parent, request, student_addr, lecturer_name, client_socket):
        super().__init__(parent, bg="#fae0e4")
        self.title("Ticket Details")
        self.parent = parent
        self.request = request
        self.lecturer_name = lecturer_name
        self.client_socket = client_socket
        self.student_addr = student_addr
        self.conversation = []

        window_width = 500
        window_height = 450

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window size and position relative to main window
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        student_id = request['student']['student_id']
        seat_no = request['student']['seat_no']
        topic = request['topic']
        priority = request['priority']
        description = request['description']

        ticket_details = tk.Text(self, wrap="word", width=70, height=6, font=("Arial", 15), bg="#fae0e4")
        ticket_details.pack()

        details = f"Student ID: {student_id}\nSeat No: {seat_no}\nLecture Name: {parent.lecturer_name}\nTopic: {topic}\nUrgency: {priority}\nDescription: {description}"
        ticket_details.insert(tk.END, details)
        ticket_details.config(state="disabled")

        chat_history_label = tk.Label(self, text="Chat:", font=("Arial", 15), bg="#fae0e4")
        chat_history_label.pack()
        self.message_history = scrolledtext.ScrolledText(self, wrap="word", width=68, height=10)
        self.message_history.pack()
        self.message_history.config(state="disabled")

        message_label = tk.Label(self, text="Message:", font=("Arial", 15), bg="#fae0e4")
        message_label.pack()
        self.message_text = tk.Text(self, wrap="word", width=70, height=5)
        self.message_text.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.RIGHT, padx=10, pady=5)

        mark_as_complete_button = tk.Button(button_frame, text="Mark as Complete", command=self.mark_as_complete)
        mark_as_complete_button.pack(side=tk.LEFT)

        send_button = tk.Button(button_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.LEFT)

        self.message_text.bind("<Return>", self.handle_enter_key)

    def mark_as_complete(self):
        # Sends chat_log to host, changes the request priority to complete and closes the chat gui
        self.send_chat_log_to_server()
        self.client_socket.change_request_priority(self.student_addr, "complete", self.conversation)
        self.master.remove_chat_from_chat_list(self.student_addr)
        self.destroy()
        print(f"{self.student_addr} Chat completed and stopped ")

    def send_chat_log_to_server(self):
        # Formats the chat_log list before sending to server
        chat_log = ["-------------------------Request Details-------------------------\n",
                    f"Topic: {self.request['topic']}\n", f"Priority: {self.request['priority']}\n",
                    f"Description: {self.request['description']}\n", f"Time: {self.request['time']}\n",
                    f"Student Id: {self.request['student']['student_id']}\n",
                    f"Seat No: {self.request['student']['seat_no']}\n",
                    f"Course No: {self.request['student']['course_no']}\n", f"Lecturer Name: {self.lecturer_name}\n",
                    "\nChat History:\n"]
        conversation_data = "".join(self.conversation)
        chat_log.append(conversation_data)

        self.client_socket.send_chat_log(chat_log)

    def update_chat_history(self, user_name, message_text):
        # Formats the message string and updates textarea in the gui
        formatted_message = f"{user_name}:{message_text}"
        self.conversation.append(formatted_message)
        self.message_history.config(state="normal")  # Enable editing
        self.message_history.insert(tk.END, formatted_message)
        self.message_history.config(state="disabled")  # Disable editing
        self.message_history.yview_moveto(1.0)

    def send_message(self):
        message = self.message_text.get("1.0", tk.END)
        if not message.strip():  # Check if the message contains only whitespace characters
            # The message is empty, do nothing
            return
        student_id = self.request['student']['student_id']
        student_addr = self.request['student']['addr']

        try:
            self.client_socket.send_message_to_student(student_id, student_addr, message)
            # Update the chat history
            self.update_chat_history(self.lecturer_name, message)
            self.message_text.delete("1.0", tk.END)

        except Exception as e:
            print(e)

    def handle_enter_key(self, event):
        self.send_message()
        return "break"
