import socket
import threading
import json
from Host import Host
from Student import Student


HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
host = Host()

student_list = []


def handle_client(conn, addr):
    print(f"New Connection from {addr}")
    client_addr = addr
    connected = True

    while connected:
        data = receive_message(conn)
        if not data:
            # If data is None, the client has disconnected
            break

        message_type = data.get("type")
        message_data = data.get("data")

        if message_type == "!COURSE_LIST":
            # Perform action for HEADER1
            print(f"{addr}: {message_data}")
            course_dict_keys = list(host.course_dict.keys())
            response = json.dumps(course_dict_keys)
            send_message(conn, "COURSE_LIST", response)

        elif message_type == "!LOGIN":
            # Handle the login details
            student_id = message_data.get("student_id")
            seat_no = message_data.get("seat_no")
            course_no = message_data.get("course_no")

            new_student = Student(student_id,seat_no,course_no,addr)
            student_list.append(new_student)
            print(
                f"{addr}: Student ID: {student_id}, Seat No: {seat_no}, Course No: {course_no}")
            print(f"Total Students: {len(student_list)}: Student ID: {student_id}")

        elif message_type == "HEADER2":
            # Perform action for HEADER2
            print(f"{addr} Received HEADER2 message:", message_data)
            # You can add your custom handling for HEADER2 here

        elif message_type == "!DISCONNECT":
            print(f"{addr} Received !DISCONNECT message:", message_data)
            connected = False

        else:
            # Unknown message type
            print(f"{addr} Unknown message type:", message_type)

    conn.close()


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
    body = sock.recv(body_length).decode(FORMAT)

    return json.loads(body)


def start():
    server.listen()
    print(f"[Listening] Server is listening on {SERVER}")
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"{threading.active_count() - 1} active connections")
    except KeyboardInterrupt:
        print("Server interrupted. Shutting down...")
    finally:
        server.close()


start()
