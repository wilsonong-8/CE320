import tkinter as tk
from tkinter import ttk


class AppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Student Helper')
        self.root.geometry('800x600')

        self.label = tk.Label(self.root, text="Student Log In", font=("Arial", 40))
        self.label.pack()

        self.student_label = tk.Label(self.root, text="Student Id", font=("Arial", 20))
        self.student_label.pack()
        self.student_id_input = ttk.Entry(master=self.root)
        self.student_id_input.pack()

        self.seat_label = tk.Label(self.root, text="Seat No", font=("Arial", 20))
        self.seat_label.pack()
        self.seat_input = ttk.Entry(master=self.root)
        self.seat_input.pack()

        self.course_label = tk.Label(self.root, text="Course", font=("Arial", 20))
        self.course_label.pack()
        self.course_input = ttk.Combobox(master=self.root, state="readonly")
        self.course_input.pack()

        self.button = ttk.Button(master=self.root, text='Submit', command=self.submit)
        self.button.pack()

    def set_course_list(self, course_list):
        self.course_input["values"] = course_list

    def submit(self):
        student_id = self.student_id_input.get()
        seat_no = self.seat_input.get()
        course_no = self.course_input.get()
        print(f"{student_id} + {seat_no} + {course_no}")
        return student_id, seat_no, course_no


    def run(self):
        self.root.mainloop()


