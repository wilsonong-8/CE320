import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import textwrap


class HandleRequestPage(tk.Frame):
    def __init__(self, parent, client_socket):
        super().__init__(parent, bg="#fae0e4")
        self.client_socket = client_socket
        self.lecturer_name = None
        self.request_list = []
        self.request_dict = {}  # Line numbers mapped to requests

        self.labels_frame = tk.Frame(self, bg="#fae0e4")  # Create a frame to wrap the labels
        self.labels_frame.pack(pady=10)

        self.lecturer_name_label = tk.Label(self.labels_frame, text="Lecturer Name:", font=("Arial", 15), bg="#fae0e4")
        self.lecturer_name_label.pack(side=tk.TOP)

        self.request_title_label = tk.Label(self.labels_frame, text="Request List", font=("Arial", 20), bg="#fae0e4")
        self.request_title_label.pack()

        self.request_listbox = ScrolledText(self.labels_frame, width=70, height=15, wrap="word")
        self.request_listbox.pack()

        self.broadcast_label = tk.Label(self.labels_frame, text="Broadcast Message:", font=("Arial", 20), bg="#fae0e4")
        self.broadcast_label.pack()

        self.broadcast_text = tk.Text(self.labels_frame, width=40, height=5)
        self.broadcast_text.pack()

        self.broadcast_text.bind("<Return>", self.handle_enter_key)

        self.send_button = tk.Button(self.labels_frame, text="Send", command=self.send_broadcast)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.request_listbox.tag_configure("working", background="grey", foreground="white")
        self.request_listbox.tag_configure("complete", background="green", foreground="white")

        self.request_listbox.tag_configure("high", background="red", foreground="white")
        self.request_listbox.tag_configure("medium", background="orange", foreground="black")
        self.request_listbox.tag_configure("low", background="yellow", foreground="black")

        # Bind the event only for high, medium, and low priority requests
        for tag in ["high", "medium", "low"]:
            self.request_listbox.tag_bind(tag, "<Button-1>", self.show_ticket_details)

        for tag in ["complete"]:
            self.request_listbox.tag_bind(tag, "<Button-1>", self.open_past_conversation)

        self.request_listbox.config(state="disabled", cursor="hand2")
        # Bind the hand cursor style to the Enter (hover) event
        self.request_listbox.bind("<Enter>", self.change_cursor_hand)
        # Bind the default cursor style to the Leave (unhover) event
        self.request_listbox.bind("<Leave>", self.change_cursor_default)

    def update_labels(self, lecturer_name, request_list):
        self.lecturer_name = lecturer_name
        self.lecturer_name_label.config(text=f"Lecturer Name: {lecturer_name}")
        self.update_request_listbox(request_list)

    def update_request_listbox(self, request_list):
        self.request_listbox.config(state="normal")  # Set as editable before changing content
        self.request_list = request_list
        self.request_listbox.delete(1.0, tk.END)
        self.request_dict.clear()

        line_num = 1
        for request in request_list:
            topic = request['topic']
            priority = request['priority']
            time = request['time']
            student_info = request['student']
            student_id = student_info['student_id']
            seat_no = student_info['seat_no']
            addr = student_info['addr']

            entry = f"Time: {time}\nPriority: {priority}\nTopic: {topic}\nStudent ID: {student_id}\nSeat No: {seat_no}\n"
            wrapped_entry = textwrap.fill(entry, width=60)

            tag = ""
            if priority == "HIGH":
                tag = "high"
            elif priority == "MEDIUM":
                tag = "medium"
            elif priority == "LOW":
                tag = "low"
            elif priority == "WORKING":
                tag = "working"
            elif priority == "COMPLETE":
                tag = "complete"

            self.request_listbox.insert(tk.END, wrapped_entry + "\n", tag)

            entry_lines = wrapped_entry.count('\n')
            for _ in range(entry_lines + 1):
                self.request_dict[line_num] = request
                line_num += 1

        self.request_listbox.config(state="disabled")  # Set as editable before changing content

    def send_broadcast(self):
        broadcast_text_content = self.broadcast_text.get("1.0", tk.END).strip()
        if broadcast_text_content:
            # Adding the lecturer's name as an argument
            self.client_socket.send_broadcast_message(self.lecturer_name, broadcast_text_content)
            self.broadcast_text.delete("1.0", tk.END)

    def show_ticket_details(self, event):
        clicked_line = int(self.request_listbox.index("@%d,%d" % (event.x, event.y)).split('.')[0])
        request = self.request_dict.get(clicked_line)
        print(request)
        if request is None:
            return
        student_addr = request['student']['addr']
        self.client_socket.change_request_priority(student_addr, "working", "")
        self.client_socket.start_chat_with_student(student_addr)
        self.master.start_chat_with_student(request, student_addr)

    def open_past_conversation(self, event):
        clicked_line = int(self.request_listbox.index("@%d,%d" % (event.x, event.y)).split('.')[0])
        request = self.request_dict.get(clicked_line)
        if request is None:
            return
        conversation = request['conversation']
        self.master.open_past_conversation(conversation)

    def change_cursor_hand(self, event):
        # Change the cursor style to hand pointer
        self.request_listbox.config(cursor="hand2")

    def change_cursor_default(self, event):
        # Change the cursor style to default
        self.request_listbox.config(cursor="")

    def handle_enter_key(self, event):
        self.send_broadcast()
        return "break"
