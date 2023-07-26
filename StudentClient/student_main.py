import tkinter as tk
from client_socket import ClientSocket
from login_page import LoginPage
from request_page import RequestPage
from waiting_page import WaitingPage

class StudentClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Student Client')
        self.geometry('800x600')

        self.client_socket = ClientSocket()

        self.student_id = None
        self.seat_no = None
        self.course_no = None

        self.login_page = LoginPage(self, self.client_socket)
        self.login_page.pack()

        # Initialize other frames but keep them hidden for now
        self.request_page = RequestPage(self, self.client_socket)
        self.request_page.pack_forget()

        self.waiting_page = WaitingPage(self,self.client_socket)
        self.waiting_page.pack_forget()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Call the disconnect method of the client_socket to safely close the socket
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

        # Show request page
        self.request_page.pack()

    def from_request_to_waiting_page(self):
        self.request_page.pack_forget()
        self.waiting_page.update_labels(self.student_id,self.seat_no,self.course_no)
        self.waiting_page.pack()

    def show_login_page(self):
        # Hide the request page
        self.request_page.pack_forget()

        # Show the login page
        self.login_page.pack()


if __name__ == '__main__':
    app = StudentClientApp()
    app.mainloop()
