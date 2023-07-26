import tkinter as tk
from tkinter import ttk, messagebox


class LoginPage(tk.Frame):
    def __init__(self, parent, client_socket):
        super().__init__(parent)
        self.client_socket = client_socket

        self.label = tk.Label(self, text="Lecture Name:", font=("Arial", 20))
        self.label.pack(pady=20)

        self.lecturer_name_entry = tk.Entry(self, font=("Arial", 20))
        self.lecturer_name_entry.pack(pady=10)

        self.login_button = tk.Button(self, text="Login", font=("Arial", 20), command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        lecturer_name = self.lecturer_name_entry.get()
        try:
            self.client_socket.submit_login(lecturer_name)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


