import tkinter as tk
from tkinter import scrolledtext


class ChatPage(tk.Frame):

    def __init__(self, parent, client_socket):
        super().__init__(parent, bg="#edf6f9")
        self.client_socket = client_socket
        self.lecturer_name = None
        self.lecturer_addr = None

        self.labels_frame = tk.Frame(self, bg="#edf6f9")  # Create a frame to wrap the labels

        self.student_id_label = tk.Label(self.labels_frame, text="Student ID:", font=("Arial", 15), bg="#edf6f9")
        self.seat_no_label = tk.Label(self.labels_frame, text="Seat No:", font=("Arial", 15), bg="#edf6f9")
        self.course_no_label = tk.Label(self.labels_frame, text="Course No:", font=("Arial", 15), bg="#edf6f9")

        self.student_id_label.pack(side=tk.TOP)
        self.seat_no_label.pack(side=tk.TOP)
        self.course_no_label.pack(side=tk.TOP)

        self.labels_frame.pack(pady=10)

        # Add a text widget to show the ticket details in the new window
        self.ticket_details = tk.Text(self, wrap="word", width=50, height=6, font=("Arial", 15), bg="#edf6f9")
        self.ticket_details.pack()

        self.message_history = scrolledtext.ScrolledText(self, wrap="word", width=68, height=10)
        self.message_history.pack()
        self.message_history.configure(state="disabled")

        # Create the message label and text box
        self.message_label = tk.Label(self, text="Message:", font=("Arial", 15), bg="#edf6f9")
        self.message_label.pack()

        self.message_text = tk.Text(self, wrap="word", width=70, height=3)
        self.message_text.pack()

        # Create the buttons at the bottom right of the text box
        self.button_frame = tk.Frame(self, bg="#edf6f9")
        self.button_frame.pack(side=tk.RIGHT, padx=10)

        self.send_button = tk.Button(self.button_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.message_text.bind("<Return>", self.handle_enter_key)

    def update_labels(self, student_id, seat_no, course_no, topic_choice, priority_choice, description):
        # Update the labels with the provided values
        self.student_id_label.config(text=f"Student ID: {student_id}")
        self.seat_no_label.config(text=f"Seat No: {seat_no}")
        self.course_no_label.config(text=f"Course No: {course_no}")

        details = f"Lecturer Name: {self.lecturer_name}\nTopic: {topic_choice}" \
                  f"\nUrgency: {priority_choice}\nDescription: {description}"
        self.ticket_details.config(state="normal")
        self.ticket_details.delete("1.0", tk.END)
        self.ticket_details.insert(tk.END, details)
        self.ticket_details.config(state="disabled")

    def set_lecturer_details(self, lecturer_name, lecturer_addr):
        self.lecturer_name = lecturer_name
        self.lecturer_addr = lecturer_addr

    def update_chat_history(self, user_name, message_text):
        formatted_message = f"{user_name}: {message_text}"
        self.message_history.config(state="normal")  # Enable editing
        self.message_history.insert(tk.END, formatted_message)
        self.message_history.config(state="disabled")  # Disable editing
        self.message_history.yview_moveto(1.0)

    def send_message(self):
        message = self.message_text.get("1.0", tk.END)
        if not message.strip():  # Check if the message contains only whitespace characters
            # The message is empty, do nothing
            return
        try:
            self.client_socket.send_message_to_lecturer(self.lecturer_name, self.lecturer_addr, message)
            # print(f"Sending message to Lecturer {self.lecturer_name} at {self.lecturer_addr}: {message}")

            self.update_chat_history("Me", message)
            self.message_text.delete("1.0", tk.END)

        except Exception as e:
            print(e)

    def delete_all_conversation(self):
        self.message_text.delete("1.0", tk.END)
        self.message_history.config(state="normal")  # Enable editing
        self.message_history.delete("1.0", tk.END)  # Delete all contents
        self.message_history.config(state="disabled")  # Disable editing

    def handle_enter_key(self, event):
        self.send_message()
        return "break"


if __name__ == '__main__':
    # Create the main application window
    root = tk.Tk()
    root.title("Chat Page")
    root.title('Student Client')
    root.geometry('800x600')

    # Instantiate the ChatPage class
    client_socket = None  # Replace with your client socket instance
    chat_page = ChatPage(root, client_socket)

    # Pack the ChatPage into the main application window
    chat_page.pack(fill=tk.BOTH, expand=True)

    # Start the main event loop
    root.mainloop()