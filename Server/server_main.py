import socket
import threading
import json
from Host import Host
from Student import Student
from Lecturer import Lecturer
from Request import Request


HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
host = Host()





def handle_client(conn, addr):
    print(f"[New Connection] from {addr} ")
    current_student = None
    current_lecturer = None
    connected = True

    while connected:
        data = receive_message(conn)
        if not data:
            # If data is None, the client has disconnected
            break

        message_type = data.get("type")
        message_data = data.get("data")

        if message_type == "!COURSE_LIST":
            course_dict_keys = list(host.course_dict.keys())
            response = json.dumps(course_dict_keys)
            send_message(conn, "COURSE_LIST", response)

        elif message_type == "!LOGIN":
            # Handle the login details
            student_id = message_data.get("student_id")
            seat_no = message_data.get("seat_no")
            course_no = message_data.get("course_no")

            current_student = Student(student_id,seat_no,course_no,addr)
            host.student_list.append(current_student)

            course_topic = host.course_dict.get(course_no)
            response_data = {"course_topic": course_topic}
            send_message(conn, "!COURSE_TOPIC", response_data)
            print(
                f"[Student Log In]{addr}: Student ID: {student_id}, Seat No: {seat_no}, Course No: {course_no}")
            print(f"[Total Students] {len(host.student_list)}")

        elif message_type == "!LOGIN_LECTURER":
            lecturer_name = message_data.get("lecturer_name")
            current_lecturer = Lecturer(lecturer_name)
            host.lecturer_list.append(current_lecturer)

            request_list = host.request_list
            response_data = {"request_list": request_list}
            send_request(conn,"!REQUEST_LIST", response_data)

            print(f"[Lecturer Log In]{addr} Lecturer Name: {lecturer_name}")
            print(f"[Total Lecturers] {len(host.lecturer_list)}")

        elif message_type == "!REQUEST":
            # Handle request from student client
            topic_choice = message_data.get("topic_choice")
            priority_choice = message_data.get("priority_choice")
            description = message_data.get("description")

            new_request = Request(topic_choice, priority_choice, description, current_student)
            host.request_list.append(new_request)

            print(f"[New Request]Student: {new_request.student.student_id}, Topic: {new_request.topic}, "
                  f"Priority: {new_request.priority.name}, Time: {new_request.time}")

        elif message_type == "HEADER2":
            # Perform action for HEADER2
            print(f"{addr} Received HEADER2 message:", message_data)
            # You can add your custom handling for HEADER2 here

        elif message_type == "!DISCONNECT":
            print(f"[Client Disconnect]:", {addr})
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


def send_request(sock, message_type, message_data):
    data = {"type": message_type, "data": message_data}
    message = json.dumps(data, cls=Request.RequestEncoder)  # Use the custom encoder
    message = f"{len(message):<{HEADER}}" + message
    sock.send(message.encode(FORMAT))


def run_server():
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


if __name__ == "__main__":
    run_server()
