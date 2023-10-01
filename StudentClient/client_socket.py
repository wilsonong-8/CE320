import socket
import json
import threading


class ClientSocket:
    def __init__(self, student_app):
        self.HEADER = 1024
        self.PORT = 5051
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.student_app = student_app
        self.connected = False
        self.start_threading()

    def disconnect(self):
        self.send_message("!DISCONNECT", "Client disconnecting")

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

    def submit_login_details(self, student_id, seat_no, course_no):
        login_details = {
            "student_id": student_id,
            "seat_no": seat_no,
            "course_no": course_no
        }
        self.send_message("!LOGIN_STUDENT", login_details)

    def submit_request(self, topic_choice, priority_choice, description):
        request_details = {
            "topic_choice": topic_choice,
            "priority_choice": priority_choice,
            "description": description
        }
        self.send_message("!REQUEST_FROM_STUDENT", request_details)

    def send_message_to_lecturer(self, lecturer_name, lecturer_addr, message):
        message_data = {
            "lecturer_name": lecturer_name,
            "lecturer_addr": lecturer_addr,
            "message": message
        }
        self.send_message("!SEND_MESSAGE_TO_LECTURER", message_data)

    def stop_threading(self):
        self.connected = False

    def start_threading(self):
        self.connected = True
        response_thread = threading.Thread(target=self.listen_for_response)
        response_thread.start()

    def listen_for_response(self):
        while self.connected:
            message = self.receive_message()
            if message is not None:
                if message["type"] == "!START_CHAT":
                    lecturer_name = message["data"]["lecturer_name"]
                    lecturer_addr = message["data"]["lecturer_addr"]
                    # Transition to the chat window here
                    self.student_app.from_waiting_page_to_chat_page(lecturer_name, lecturer_addr)

                elif message["type"] == "!CHAT_WITH_LECTURER":
                    lecturer_name = message["data"]["lecturer_name"]
                    message = message["data"]["message"]
                    print(f"{lecturer_name}: {message}")
                    # Implement appending of chat messages to the textarea
                    self.student_app.on_receive_message(lecturer_name, message)

                elif message["type"] == "!COURSE_LIST":
                    # Handle receiving and processing the course list
                    course_list = json.loads(message["data"])
                    print("Received Course List:", course_list)
                    self.student_app.on_receive_course_list(course_list)

                elif message["type"] == "!COURSE_TOPIC":
                    # Handle receiving and processing the course topic
                    course_topic = message["data"]["course_topic"]
                    print("Received Course Topic:", course_topic)
                    self.student_app.from_login_to_request_page(course_topic)

                elif message["type"] == "!END_CHAT":
                    # Handle ending a chat session
                    self.student_app.from_chat_page_to_request_page()

                elif message["type"] == "!BROADCAST_MESSAGE":
                    broadcast_message = message["data"]["message"]
                    # Display the broadcast message as a pop-up or alert
                    self.student_app.display_broadcast_message(broadcast_message)


