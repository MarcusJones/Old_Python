import socket
from sockets_playground import get_local_ip
SERVER_IP = "192.168.1.3"

class Client():
    def __init__(self,address=(SERVER_IP,5000)):
        self.s = socket.socket()
        self.s.connect(address)

TC=Client()