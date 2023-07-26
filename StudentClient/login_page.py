import tkinter as tk
from tkinter import ttk, messagebox


class LoginPage(tk.Frame):
    def __init__(self, parent, client_socket):
        super().__init__(parent)
        self.client_socket = client_socket

        self.label = tk.Label(self, text="Student Log In", font=("Arial", 40))
        self.label.pack()

        self.student_label = tk.Label(self, text="Student Id", font=("Arial", 20))
        self.student_label.pack()
        self.student_id_input = ttk.Entry(master=self)
        self.student_id_input.pack()

        self.seat_label = tk.Label(self, text="Seat No", font=("Arial", 20))
        self.seat_label.pack()
        self.seat_input = ttk.Entry(master=self)
        self.seat_input.pack()

        self.course_label = tk.Label(self, text="Course", font=("Arial", 20))
        self.course_label.pack()
        self.course_input = ttk.Combobox(master=self, state="readonly")
        self.course_input.pack()

        self.button = ttk.Button(master=self, text='Submit', command=self.submit_student_info)
        self.button.pack()

        self.set_course_list()

    def set_course_list(self):
        try:
            course_list = self.client_socket.retrieve_course_list()
            self.course_input["values"] = course_list
            # self.course_input.set(course_list[0])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def submit_student_info(self):
        student_id = self.student_id_input.get()
        seat_no = self.seat_input.get()
        course_no = self.course_input.get()
        try:
            course_topic = self.client_socket.submit_login_details(student_id,seat_no,course_no)
            self.master.from_login_to_request_page(course_topic)
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Unable to retrieve Topics, please approach the Lecturer")
