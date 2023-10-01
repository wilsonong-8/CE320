import tkinter as tk

from client_socket import ClientSocket
from login_page import LoginPage
from handle_request_page import HandleRequestPage
from lecturer_chat import LecturerChat
from past_conversation_page import PastConversation


class LecturerClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Lecturer Client')
        self.geometry('700x600')
        self.configure(bg="#fae0e4")

        self.client_socket = ClientSocket(self)

        self.lecturer_name = None
        self.chat_list = []

        self.login_page = LoginPage(self, self.client_socket)
        self.login_page.pack()

        # Initialize other frames but keep them hidden for now
        self.handle_request_page = HandleRequestPage(self, self.client_socket)
        self.handle_request_page.pack_forget()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Call the disconnect method of the client_socket to safely close the socket
        self.client_socket.stop_threading()
        self.client_socket.disconnect()
        self.destroy()

    def from_login_to_request_page(self, request_list):
        # Hide the login page
        self.login_page.pack_forget()

        # Show the request list page
        self.lecturer_name = self.login_page.lecturer_name_entry.get()
        self.handle_request_page.update_labels(self.lecturer_name, request_list)

        # Show request page
        self.handle_request_page.pack()

    def update_request_list(self, request_list):
        self.handle_request_page.update_request_listbox(request_list)

    def start_chat_with_student(self, request, student_addr):
        new_chat_page = LecturerChat(self, request, student_addr, self.lecturer_name, self.client_socket, )
        self.chat_list.append(new_chat_page)

    def find_and_update_chat_history_(self, student_id, student_addr, message):
        for lecturer_chat in self.chat_list:
            if isinstance(lecturer_chat, LecturerChat) and lecturer_chat.student_addr == student_addr:
                lecturer_chat.update_chat_history(student_id, message)

    def remove_chat_from_chat_list(self, student_addr):
        self.chat_list = [chat for chat in self.chat_list if chat.student_addr != student_addr]

    def open_past_conversation(self, conversation):
        PastConversation(self, conversation)


if __name__ == '__main__':
    app = LecturerClientApp()
    app.mainloop()
