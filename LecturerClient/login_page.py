import tkinter as tk
from tkinter import ttk, messagebox


class LoginPage(tk.Frame):
    def __init__(self, parent, client_socket):
        # Initialize the LoginPage class
        super().__init__(parent, bg="#fae0e4")

        # Store the client socket reference
        self.client_socket = client_socket

        # Create and pack widgets
        self.label = tk.Label(self, text="Lecturer Login", font=("Arial", 40), bg="#fae0e4")
        self.label.pack(pady=20)

        self.lecturer_label = tk.Label(self, text="Lecturer Name", font=("Arial", 20), bg="#fae0e4")
        self.lecturer_label.pack()
        self.lecturer_name_entry = tk.Entry(self, font=("Arial", 20))
        self.lecturer_name_entry.pack(pady=10)

        self.login_button = tk.Button(self, text="Login", font=("Arial", 20), command=self.login)
        self.login_button.pack(pady=20)

    def is_valid_input(self, input_value):
        # Check if input_value is not empty or contains only spaces
        return bool(input_value.strip())

    def login(self):
        # Get the lecturer's name from the entry widget
        lecturer_name = self.lecturer_name_entry.get()

        # Check if the input is valid
        if not self.is_valid_input(lecturer_name):
            messagebox.showerror("Invalid Input", "Please enter the lecturer name.")
            return

        try:
            # Submit the login request to the client socket
            self.client_socket.submit_login(lecturer_name)

        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"An error occurred: {str(e)}")