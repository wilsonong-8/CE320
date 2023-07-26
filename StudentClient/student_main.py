import tkinter as tk
from client_socket import ClientSocket
from login_page import LoginPage

if __name__ == '__main__':
    client_socket = ClientSocket()

    root = tk.Tk()
    root.title('Student Client')
    root.geometry('800x600')

    login_page = LoginPage(root,client_socket)
    login_page.pack()

    root.mainloop()