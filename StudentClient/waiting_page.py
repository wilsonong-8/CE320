import tkinter as tk

class WaitingPage(tk.Frame):
    def __init__(self, parent, client_socket):
        super().__init__(parent, bg="#edf6f9")
        self.client_socket = client_socket

        # Create a frame to wrap the labels
        self.labels_frame = tk.Frame(self, bg="#edf6f9")
        self.labels_frame.pack(pady=10)

        # Labels to display student information
        self.student_id_label = tk.Label(self.labels_frame, text="Student ID:", font=("Arial", 15), bg="#edf6f9")
        self.seat_no_label = tk.Label(self.labels_frame, text="Seat No:", font=("Arial", 15), bg="#edf6f9")
        self.course_no_label = tk.Label(self.labels_frame, text="Course No:", font=("Arial", 15), bg="#edf6f9")

        # Pack labels within the labels frame
        self.student_id_label.pack(side=tk.TOP)
        self.seat_no_label.pack(side=tk.TOP)
        self.course_no_label.pack(side=tk.TOP)

        # Label to indicate waiting for lecturer
        self.label = tk.Label(self, text="Waiting For Lecturer...", font=("Arial", 40), bg="#edf6f9")
        self.label.pack()

    def update_labels(self, student_id, seat_no, course_no):
        # Update the labels with the provided values
        self.student_id_label.config(text=f"Student ID: {student_id}")
        self.seat_no_label.config(text=f"Seat No: {seat_no}")
        self.course_no_label.config(text=f"Course No: {course_no}")
