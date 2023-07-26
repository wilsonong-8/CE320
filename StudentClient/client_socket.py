import socket
import json

class ClientSocket:
    def __init__(self):
        self.HEADER = 1024
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

    def disconnect(self):
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

    def retrieve_course_list(self):
        self.send_message("!COURSE_LIST", "Here to retrieve Course List")
        message = self.receive_message()

        if message["type"] == "COURSE_LIST":
            course_list = json.loads(message["data"])
            print("Received Course List:", course_list)
            return course_list

    def submit_login_details(self, student_id, seat_no, course_no):
        login_details = {
            "student_id": student_id,
            "seat_no": seat_no,
            "course_no": course_no
        }
        self.send_message("!LOGIN", login_details)
