import tkinter as tk
from tkinter import ttk,messagebox


class RequestPage(tk.Frame):

    def __init__(self, parent, client_socket):
        super().__init__(parent)
        self.client_socket = client_socket
        priority_list = ["Super Urgent", "I have a question", "I need some information"]
        self.student_id = None
        self.seat_no = None
        self.course_no = None

        self.labels_frame = tk.Frame(self)  # Create a frame to wrap the labels
        self.labels_frame.pack(pady=10)

        self.student_id_label = tk.Label(self.labels_frame, text="Student ID:", font=("Arial", 15))
        self.seat_no_label = tk.Label(self.labels_frame, text="Seat No:", font=("Arial", 15))
        self.course_no_label = tk.Label(self.labels_frame, text="Course No:", font=("Arial", 15))

        self.student_id_label.pack(side=tk.TOP)
        self.seat_no_label.pack(side=tk.TOP)
        self.course_no_label.pack(side=tk.TOP)

        self.label = tk.Label(self, text="Ask For Help", font=("Arial", 40))
        self.label.pack()

        self.topic_label = tk.Label(self, text="Topic", font=("Arial", 20))
        self.topic_label.pack()
        self.topic_input = ttk.Combobox(master=self, state="readonly")
        self.topic_input.pack()

        self.priority_label = tk.Label(self, text="Priority", font=("Arial", 20))
        self.priority_label.pack()
        self.priority_input = ttk.Combobox(master=self, state="readonly")
        self.priority_input["values"] = priority_list
        self.priority_input.pack()
        # self.priority_input.set(priority_list[0])

        self.description_label = tk.Label(self, text="Description", font=("Arial", 20))
        self.description_label.pack()
        self.description_input = tk.Text(master=self, width=30, height=3, font=("Arial", 14))
        self.description_input.pack()

        self.button = ttk.Button(master=self, text='Submit', command=self.submit_request)
        self.button.pack()

    def set_course_topic(self, course_topic):
        self.topic_input["values"] = course_topic
        # self.topic_input.set(course_topic[0])

    def update_labels(self, student_id, seat_no, course_no):
        # Update the labels with the provided values
        self.student_id_label.config(text=f"Student ID: {student_id}")
        self.seat_no_label.config(text=f"Seat No: {seat_no}")
        self.course_no_label.config(text=f"Course No: {course_no}")

    def submit_request(self):
        topic_choice = self.topic_input.get()
        priority_choice = self.priority_input.get()
        description = self.description_input.get("1.0", "end-1c")
        try:
            self.client_socket.submit_request(topic_choice, priority_choice, description)
            # TRANSITION FROM REQUEST TO WAITING PAGE
            self.master.from_request_to_waiting_page()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"Unable to send Request: {e}")


