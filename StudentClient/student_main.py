import socket
import json
from student_gui import AppGUI

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


def send_message(sock, message_type, message_data):
    data = {"type": message_type, "data": message_data}
    message = json.dumps(data)
    message = f"{len(message):<{HEADER}}" + message
    sock.send(message.encode(FORMAT))


def receive_message(sock):
    header = sock.recv(HEADER).decode(FORMAT)
    if not header:
        return None
    body_length = int(header.strip())
    body = sock.recv(body_length).decode()
    return json.loads(body)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(client)
try:
    """
    Initializes the Student GUI
    Sends out message to retrieve CourseList from Server to populate Course ComboBox
    Then starts the GUI
    """
    app_gui = AppGUI()
    send_message(client, "!COURSE_LIST", "Here to retrieve Course List")
    message = receive_message(client)

    if message["type"] == "COURSE_LIST":
        course_list = json.loads(message["data"])
        print("Received Course List:", course_list)
        app_gui.set_course_list(course_list)

    student_info = app_gui.submit()
    print(student_info)

    app_gui.run()

    while True:
        user_input = input("Enter a message (type !DISCONNECT to exit): ")
        if user_input == DISCONNECT_MESSAGE:
            send_message(client, "!DISCONNECT", "Client is Disconnecting")
            break
        #Change this code accordingly
        elif user_input == "HEADER1":
            send_message(client, "HEADER1", "Hello Server, this is HEADER1")
            message = receive_message(client)
            if message["type"] == "COURSE_LIST":
                course_list = json.loads(message["data"])
                print("Received Course List:", course_list)
        else:
            send_message(client, "STRING", user_input)
            message = receive_message(client)
            if message["type"] == "STRING_REPLY":
                print(f"Received STRING Reply: {message['data']}")

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    client.close()


