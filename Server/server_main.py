import socket
import threading
import json
from Host import Host
from Student import Student
from Lecturer import Lecturer
from Request import Request

# Constants for the server configuration
HEADER = 1024
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Initialize the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
host = Host()


# Handles communication between Server and Clients using json as mode of communication with a header and data
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
            # Respond with the list of available courses
            course_dict_keys = list(host.course_dict.keys())
            response = json.dumps(course_dict_keys)
            send_message(conn, "!COURSE_LIST", response)

        elif message_type == "!LOGIN_STUDENT":
            # Handle student login details
            student_id = message_data.get("student_id")
            seat_no = message_data.get("seat_no")
            course_no = message_data.get("course_no")

            # Create a Student instance and add it to the host's student_list
            current_student = Student(student_id,seat_no,course_no, addr, conn)
            host.student_list.append(current_student)

            course_topic = host.course_dict.get(course_no)
            response_data = {"course_topic": course_topic}
            send_message(conn, "!COURSE_TOPIC", response_data)
            print(
                f"[Student Log In]{addr} and conn{conn}: Student ID: {student_id}, Seat No: {seat_no}, Course No: {course_no}")
            print(f"[Total Students] {len(host.student_list)}")

        elif message_type == "!LOGIN_LECTURER":
            # Handle lecturer login details
            lecturer_name = message_data.get("lecturer_name")
            # Create a Lecturer instance and add it to the host's lecturer_list
            current_lecturer = Lecturer(lecturer_name, addr, conn)
            host.lecturer_list.append(current_lecturer)
            # Get the current list of requests and send it to the newly logged in lecturer
            request_list = host.request_list
            response_data = {"request_list": request_list}
            send_request(conn, "!REQUEST_LIST", response_data)
            print(f"[Lecturer Log In]{addr} Lecturer Name: {lecturer_name}")
            print(f"[Total Lecturers] {len(host.lecturer_list)}")

        elif message_type == "!REQUEST_FROM_STUDENT":
            # Handle request from student client
            topic_choice = message_data.get("topic_choice")
            priority_choice = message_data.get("priority_choice")
            description = message_data.get("description")
            # Create a new request instance based on student input
            current_student_list = [current_student.to_dict()]
            new_request = Request(topic_choice, priority_choice, description, current_student_list)
            # Insert the new request at the beginning of the request list
            host.request_list.insert(0, new_request)

            # Inform all connected lecturers about the updated request list
            for lecturer in host.lecturer_list:
                if lecturer.conn:
                    request_list = host.request_list
                    response_data = {"request_list": request_list}
                    send_request(lecturer.conn, "!UPDATE_REQUEST_LIST", response_data)
            print(f"[New Request]Student: {current_student_list[0]}, Topic: {new_request.topic}, "
                  f"Priority: {new_request.priority.name}, Time: {new_request.time}")

        elif message_type == "!CHANGE_PRIORITY":
            # Extract information from the received message
            student_addr = message_data.get("student_addr")
            priority_choice_str = message_data.get("priority")
            priority_choice = Request.static_get_priority_from_string(priority_choice_str)

            # Update the priority of the corresponding request and conversation if needed
            for request in host.request_list:
                student_info = request.student[0]
                if list(student_info["addr"]) == student_addr:
                    request.priority = priority_choice
                    if priority_choice_str == "complete":
                        request.conversation = message_data.get("conversation")
                    break  # Break out of the loop after updating the priority

            # Inform connected lecturers about the updated request list
            for lecturer in host.lecturer_list:
                if lecturer.conn:
                    request_list = host.request_list
                    response_data = {"request_list": request_list}
                    send_request(lecturer.conn, "!UPDATE_REQUEST_LIST", response_data)

            # If the priority is changed to "complete", send "End Chat" message to the student
            if priority_choice_str == "complete":
                for student in host.student_list:
                    if list(student.addr) == student_addr:
                        student_conn = student.conn
                        break
                if student_conn:
                    response_data = {
                        "message": "End Chat"
                    }
                    send_message(student_conn, "!END_CHAT", response_data)
            print(f"[Priority Changed]Changed priority for {student_addr} to {priority_choice}")

        elif message_type == "!START_CHAT":
            # Extract necessary information from the message data
            student_addr = message_data.get("student_addr")
            student_conn = None

            # Find the student's connection based on the address
            for student in host.student_list:
                if list(student.addr) == student_addr:
                    student_conn = student.conn
                    break
            if student_conn:
                # Prepare response data to initiate the chat with student
                response_data = {
                    "lecturer_name": current_lecturer.name,
                    "lecturer_addr": current_lecturer.addr,
                    "message": "Start Chat"
                }
                send_message(student_conn, "!START_CHAT", response_data)
                print(f"[Chat Started] Lecturer: {current_lecturer.name} and Student: {student.student_id}")

            else:
                print(f"[Not Found] Student with ID {student_id} and address {student_addr} not found.")

        elif message_type == "!SEND_MESSAGE_TO_STUDENT":
            student_id = message_data.get("student_id")
            student_addr = message_data.get("student_addr")
            message = message_data.get("message")
            student_conn = None

            # Find the student's connection based on the address
            for student in host.student_list:
                if list(student.addr) == student_addr:
                    student_conn = student.conn
                    break
            if student_conn:
                # Prepare response data to send the chat message to the student
                response_data = {
                    "lecturer_name": current_lecturer.name,
                    "message": message,

                }
                send_message(student_conn, "!CHAT_WITH_LECTURER", response_data)
                print(f"[Chat Sent] Lecturer: {current_lecturer.name} and Student: {student.student_id} "
                      f"and Message: {message}")
            else:
                print(f"[Not Sent] Student with ID {student_id} and address {student_addr} not found.")

        elif message_type == "!SEND_MESSAGE_TO_LECTURER":
            lecturer_name = message_data.get("lecturer_name")
            lecturer_addr = message_data.get("lecturer_addr")
            message = message_data.get("message")
            lecturer_conn = None

            # Find the lecturer's connection based on the address
            for lecturer in host.lecturer_list:
                if list(lecturer.addr) == lecturer_addr:
                    lecturer_conn = lecturer.conn
                    break
            if lecturer_conn:
                # Prepare response data to send the chat message to the lecturer
                response_data = {
                    "student_id": current_student.student_id,
                    "student_addr": current_student.addr,
                    "message": message,

                }
                send_message(lecturer_conn, "!CHAT_WITH_STUDENT", response_data)
                print(f"[Chat Sent] Student: {current_student.student_id} and Lecturer: {lecturer_name} "
                      f"and Message: {message}")
            else:
                print(f"[Not Sent] Lecturer with name {lecturer_name} and address {lecturer_addr} not found.")

        elif message_type == "!SEND_BROADCAST":
            # Extract broadcast details from the received data
            lecturer_name = message_data.get("lecturer_name")
            broadcast_message = message_data.get("broadcast_message")
            full_message = f"{lecturer_name}: {broadcast_message}"
            # Send the broadcast message to all connected students
            for student in host.student_list:
                send_message(student.conn, "!BROADCAST_MESSAGE", {"message": full_message})

        # Handle saving chat logs
        elif message_type == "!CHAT_LOG":
            chat_log = message_data.get("chat_log")
            host.save_chat_log(chat_log)
            print(f"[CHAT LOG SAVED]")

        # Handle client disconnection
        elif message_type == "!DISCONNECT":
            # Remove the student or lecturer from the appropriate list
            if current_student:
                for student in host.student_list:
                    if student.addr == addr:
                        host.student_list.remove(student)
                        break
            else:
                for lecturer in host.lecturer_list:
                    if lecturer.addr == addr:
                        host.lecturer_list.remove(lecturer)
                        break
            print(f"[Client Disconnect]:", {addr})
            connected = False

        else:
            # Handle unknown message types
            print(f"{addr} Unknown message type:", message_type)

    # Close the connection once the handling is done
    conn.close()


# Packages input parameters into header and data before converting to json and sending to client
def send_message(sock, message_type, message_data):
    data = {"type": message_type, "data": message_data}
    message = json.dumps(data)
    message = f"{len(message):<{HEADER}}" + message
    sock.send(message.encode(FORMAT))


# Receives json data and unpacking to body
def receive_message(sock):
    header = sock.recv(HEADER).decode(FORMAT)
    if not header:
        return None

    body_length = int(header.strip())
    body = sock.recv(body_length).decode(FORMAT)

    return json.loads(body)


# Uses Encoder to encode class objects into json before sending data over to client
def send_request(sock, message_type, message_data):
    data = {"type": message_type, "data": message_data}
    message = json.dumps(data, cls=Request.RequestEncoder)  # Use the custom encoder
    message = f"{len(message):<{HEADER}}" + message
    sock.send(message.encode(FORMAT))


# Starts server and listens for active connections.
# Every client connection start a thread with a unique "conn" object and "addr" port number
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
