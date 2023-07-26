import tkinter as tk
from client_socket import ClientSocket
from login_page import LoginPage

class LecturerClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Lecturer Client')
        self.geometry('1000x600')

        self.lecturer_name = None

        self.client_socket = ClientSocket()

        self.login_page = LoginPage(self, self.client_socket)
        self.login_page.pack()

        # Initialize other frames but keep them hidden for now
        # self.request_page = RequestPage(self, self.client_socket)
        # self.request_page.pack_forget()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Call the disconnect method of the client_socket to safely close the socket
        self.client_socket.disconnect()
        self.destroy()

    # def from_login_to_request_page(self, course_topic):
    #     # Hide the login page
    #     self.login_page.pack_forget()
    #
    #     self.lecturer_name = self.login_page.lecturer_name_entry.get()
    #
    #     # Show the request page and pass the course_info
    #     self.request_page.update_labels(self.student_id, self.seat_no, self.course_no)
    #     # Show request page
    #     self.request_page.pack()


if __name__ == '__main__':
    app = LecturerClientApp()
    app.mainloop()
