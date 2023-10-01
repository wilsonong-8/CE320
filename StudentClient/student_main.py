import tkinter as tk
from client_socket import ClientSocket
from login_page import LoginPage
from request_page import RequestPage
from waiting_page import WaitingPage
from chat_page import ChatPage
from tkinter import messagebox


class StudentClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Student Client')
        self.geometry('600x500')
        self.configure(bg="#edf6f9")

        # Initialize the client socket for communication
        self.client_socket = ClientSocket(self)

        # Variables to store user input data
        self.student_id = None
        self.seat_no = None
        self.course_no = None
        self.topic_choice = None
        self.priority_choice = None
        self.description = None

        # Create the login page and pack it
        self.login_page = LoginPage(self, self.client_socket)
        self.login_page.pack()

        # Initialize other frames but keep them hidden for now
        self.request_page = RequestPage(self, self.client_socket)
        self.request_page.pack_forget()

        self.waiting_page = WaitingPage(self, self.client_socket)
        self.waiting_page.pack_forget()

        self.chat_page = ChatPage(self, self.client_socket)
        self.chat_page_instance = self.chat_page
        self.chat_page.pack_forget()

        # Set the close window protocol to safely close the application
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Call methods to disconnect and close the socket
        self.client_socket.stop_threading()
        self.client_socket.disconnect()
        self.destroy()

    def from_login_to_request_page(self, course_topic):
        # Hide the login page
        self.login_page.pack_forget()

        # Show the request page and pass the course_info
        self.student_id = self.login_page.student_id_input.get()
        self.seat_no = self.login_page.seat_input.get()
        self.course_no = self.login_page.course_input.get()
        self.request_page.set_course_topic(course_topic)
        self.request_page.update_labels(self.student_id, self.seat_no, self.course_no)

        # Show the request page
        self.request_page.pack()

    def from_request_to_waiting_page(self):
        # Hide the request page
        self.request_page.pack_forget()

        # Update variables with user input data
        self.topic_choice = self.request_page.topic_input.get()
        self.priority_choice = self.request_page.priority_input.get()
        self.description = self.request_page.description_input.get("1.0", "end-1c")

        # Show the waiting page
        self.waiting_page.update_labels(self.student_id, self.seat_no, self.course_no)
        self.waiting_page.pack()

    def from_waiting_page_to_chat_page(self, lecturer_name, lecturer_addr):
        # Hide the waiting page
        self.waiting_page.pack_forget()

        # Update chat page with details and show it
        self.chat_page.set_lecturer_details(lecturer_name, lecturer_addr)
        self.chat_page.update_labels(self.student_id, self.seat_no, self.course_no, self.topic_choice,
                                     self.priority_choice, self.description)
        self.chat_page.pack()

    def from_chat_page_to_request_page(self):
        # Hide the chat page and return to the request page
        self.chat_page.delete_all_conversation()
        self.chat_page.pack_forget()
        self.request_page.pack()

    def on_receive_message(self, lecturer_name, message):
        # Update the chat history when receiving a message
        self.chat_page.update_chat_history(lecturer_name, message)

    def on_receive_course_list(self, course_list):
        # Update the course list on the login page
        self.login_page.set_course_list(course_list)

    def display_broadcast_message(self, message):
        # Display a broadcast message as a pop-up
        header = "Broadcast from Lecturer\n"
        full_message = header + message
        messagebox.showinfo("Broadcast from Lecturer", full_message, parent=self)


if __name__ == '__main__':
    app = StudentClientApp()
    app.mainloop()
