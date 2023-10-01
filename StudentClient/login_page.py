import tkinter as tk
from tkinter import ttk, messagebox
import re


class LoginPage(tk.Frame):
    def __init__(self, parent, client_socket):
        super().__init__(parent, bg="#edf6f9")
        self.client_socket = client_socket

        # Add some space between the heading label and student ID label
        self.spacing_label = tk.Label(self, text="", font=("Arial", 30), bg="#edf6f9")
        self.spacing_label.pack()

        # Label for the login page heading
        self.label = tk.Label(self, text="Student Log In", font=("Arial", 40), bg="#edf6f9")
        self.label.pack()

        # Add some space between the heading label and student ID label
        self.spacing_label = tk.Label(self, text="", font=("Arial", 40), bg="#edf6f9")
        self.spacing_label.pack()

        # Label and input field for student ID
        self.student_label = tk.Label(self, text="Student Id (CT1234567)", font=("Arial", 20), bg="#edf6f9")
        self.student_label.pack()
        self.student_id_input = ttk.Entry(master=self)
        self.student_id_input.pack()

        # Label and input field for seat number
        self.seat_label = tk.Label(self, text="Seat No(1-99)", font=("Arial", 20), bg="#edf6f9")
        self.seat_label.pack()
        self.seat_input = ttk.Entry(master=self)
        self.seat_input.pack()

        # Label and input field for selecting a course
        self.course_label = tk.Label(self, text="Course", font=("Arial", 20), bg="#edf6f9")
        self.course_label.pack()
        self.course_input = ttk.Combobox(master=self, state="readonly")
        self.course_input.pack()

        # Submit button
        self.button = ttk.Button(master=self, text='Submit', command=self.submit_student_info)
        self.button.pack()

        # Retrieve the list of courses
        self.retrieve_course_list()

    def retrieve_course_list(self):
        try:
            self.client_socket.retrieve_course_list()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def set_course_list(self, course_list):
        # Set the available course options in the combobox
        self.course_input["values"] = course_list

    def is_valid_student_id(self, student_id):
        # Validate the student ID using regex
        pattern = r'^(ct|CT)\d{7}$'
        return bool(re.match(pattern, student_id))

    def is_valid_seat_no(self, seat_no):
        # Validate the seat number using regex
        pattern = r'^\d{1,2}$'
        return bool(re.match(pattern, seat_no))

    def submit_student_info(self):
        student_id = self.student_id_input.get()
        seat_no = self.seat_input.get()
        course_no = self.course_input.get()

        if not self.is_valid_student_id(student_id):
            messagebox.showerror("Invalid Student ID", "Student ID must start with 'ct' or 'CT' followed by 7 digits.")
            return

        if not self.is_valid_seat_no(seat_no):
            messagebox.showerror("Invalid Seat No", "Seat No must be a number with maximum 2 digits.")
            return

        if not course_no:
            messagebox.showerror("Missing Course", "Please select a course.")
            return

        try:
            # Submit student login details to the client socket
            self.client_socket.submit_login_details(student_id, seat_no, course_no)
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Unable to retrieve Topics, please approach the Lecturer")
