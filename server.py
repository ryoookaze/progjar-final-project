import socket
import threading
import sys
import pickle

class Server():
	def __init__(self, host="0.0.0.0", port=4000):

		self.client = []

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((str(host), int(port)))
		self.sock.listen(10)
		self.sock.setblocking(False)
        

		accept = threading.Thread(target=self.acceptCon)
		process = threading.Thread(target=self.processCon)
		
		accept.daemon = True
		accept.start()

		process.daemon = True
		process.start()

		while True:
			msg = input('->')
			if msg == 'out':
				self.sock.close()
				sys.exit()
			else:
				pass


	def msg_to_all(self, msg, cliente):
		for c in self.client:
			try:
				if c != client:
					c.send(msg)
			except:
				self.client.remove(c)

	def acceptCon(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				conn.setblocking(False)
				self.clientes.append(conn)
			except:
				pass

	def processCon(self):
		while True:
			if len(self.client) > 0:
				for c in self.client:
					try:
						data = c.recv(1024)
						if data:
							self.msg_to_all(data,c)
					except:
						pass


s = Server()