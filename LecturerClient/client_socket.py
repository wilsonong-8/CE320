import socket
import json

class ClientSocket:
    def __init__(self):
        self.HEADER = 1024
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

    def disconnect(self):
        self.send_message("!DISCONNECT", "Client disconnecting")
        self.client.close()

    def send_message(self, message_type, message_data):
        data = {"type": message_type, "data": message_data}
        message = json.dumps(data)
        message = f"{len(message):<{self.HEADER}}" + message
        self.client.send(message.encode(self.FORMAT))

    def receive_message(self):
        header = self.client.recv(self.HEADER).decode(self.FORMAT)
        if not header:
            return None
        body_length = int(header.strip())
        body = self.client.recv(body_length).decode()
        return json.loads(body)

    def submit_login(self, lecturer_name):
        login_details = {
            "lecturer_name": lecturer_name
        }
        self.send_message("!LOGIN_LECTURER", login_details)
        message = self.receive_message()

        if message["type"] == "!REQUEST_LIST":
            request_list = message["data"]["request_list"]
            print("Received Request List:", request_list)



