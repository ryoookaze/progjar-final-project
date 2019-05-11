import socket
import threading
import sys

class server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            data =  c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                break
    
    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(a,b))
            cThread.daemon = True
            cThread.start()
            connections.appends(c)
            print(self.connections)

class client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def sendmessage(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

    def __init__(self, address):
        port = 10000
        self.sock.connect((address, port))

        inputThread = threading.Thread(target=self.sendmessage)
        inputThread.daemon = True
        inputThread.start()
        
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(data)

if(len(sys.argv) > 1):
    client = client(sys.argv[1])
else:
    server = server()
    server.run()

