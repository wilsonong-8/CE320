import socket

HEADER = 1024
PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))



send("Hello World")
input()
send("Hello Class")
input()
send("Bye Class")
input()
send(DISCONNECT_MESSAGE)


