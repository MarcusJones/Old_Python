import socket, time,os, random

class Server():
    def __init__(self,address=('',5000),max_client=1):
        # Create a socket
        self.s = socket.socket()
        self.s.bind(address)
        self.s.listen(max_client)

    def wait_for_connection(self):
        self.Client, self.Adr=(self.s.accept())
        print("Recieved connection from {}".format(self.Client))

this_server=Server()
this_server.wait_for_connection()