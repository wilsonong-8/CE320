import socket
import json
from tkinter import messagebox
import threading


class ClientSocket:
    def __init__(self, lecturer_app, ):
        # Initialize the ClientSocket class
        self.HEADER = 1024
        self.PORT = 5051
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        # Create a socket connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        # Store the reference to the lecturer application
        self.lecturer_app = lecturer_app
        # Initialize the connected status and start the response thread
        self.connected = False
        self.start_threading()

    def disconnect(self):
        # Send a disconnect message to the server
        self.send_message("!DISCONNECT", "Client disconnecting")

    def send_message(self, message_type, message_data):
        # Construct and send a message to the server
        data = {"type": message_type, "data": message_data}
        message = json.dumps(data)
        message = f"{len(message):<{self.HEADER}}" + message
        self.client.send(message.encode(self.FORMAT))

    def receive_message(self):
        # Receive and decode a message from the server
        header = self.client.recv(self.HEADER).decode(self.FORMAT)
        if not header:
            return None
        body_length = int(header.strip())
        body = self.client.recv(body_length).decode()
        return json.loads(body)

    def submit_login(self, lecturer_name):
        # Send a login request to the server
        login_details = {
            "lecturer_name": lecturer_name
        }
        self.send_message("!LOGIN_LECTURER", login_details)

    def login(self):
        lecturer_name = self.lecturer_name_entry.get()
        try:
            self.submit_login(lecturer_name)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def change_request_priority(self, student_addr, priority,conversation):
        message_data = {
            "student_addr": student_addr,
            "priority": priority,
            "conversation": conversation
        }
        self.send_message("!CHANGE_PRIORITY", message_data)

    def start_chat_with_student(self, student_addr):
        message_data = {
            "student_addr": student_addr,
        }
        self.send_message("!START_CHAT", message_data)

    def send_message_to_student(self, student_id, student_addr, message):
        message_data = {
            "student_id": student_id,
            "student_addr": student_addr,
            "message": message
        }
        self.send_message("!SEND_MESSAGE_TO_STUDENT", message_data)

    def send_broadcast_message(self, lecturer_name, broadcast_message):
        message_data = {
            "lecturer_name": lecturer_name,
            "broadcast_message": broadcast_message
        }
        self.send_message("!SEND_BROADCAST", message_data)

    def send_chat_log(self, chat_log):
        message_data = {
            "chat_log": chat_log,
        }
        self.send_message("!CHAT_LOG", message_data)

    def stop_threading(self):
        self.connected = False

    def start_threading(self):
        # Start the response listening thread
        self.connected = True
        response_thread = threading.Thread(target=self.listen_for_response)
        response_thread.start()

    def listen_for_response(self):
        # Continuously listen for server responses
        while self.connected:
            message = self.receive_message()
            if message is not None:
                # Handle incoming chat messages
                if message["type"] == "!CHAT_WITH_STUDENT":
                    student_id = message["data"]["student_id"]
                    student_addr = message["data"]["student_addr"]
                    message = message["data"]["message"]
                    # Implement appending of chat messages to the textarea
                    self.lecturer_app.find_and_update_chat_history_(student_id, student_addr, message, )

                elif message["type"] == "!REQUEST_LIST":
                    # Handle incoming request list updates
                    request_list = message["data"]["request_list"]
                    print("Received Request List:", request_list)
                    self.lecturer_app.from_login_to_request_page(request_list)

                elif message["type"] == "!UPDATE_REQUEST_LIST":
                    # Handle incoming updated request list
                    request_list = message["data"]["request_list"]
                    print("Received Updated Request List:", request_list)
                    self.lecturer_app.update_request_list(request_list)




