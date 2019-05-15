import socket
import threading
import sys
import pickle

class Server():
	def __init__(self, host="localhost", port=4000):

		self.clients = []

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((str(host), int(port)))
		self.sock.listen(10)
		self.sock.setblocking(False)

		aceptar = threading.Thread(target=self.aceptarCon)
		procesar = threading.Thread(target=self.procesarCon)
		
		aceptar.daemon = True
		aceptar.start()

		procesar.daemon = True
		procesar.start()

		while True:
			msg = input('->')
			if msg == 'out':
				self.sock.close()
				sys.exit()
			else:
				pass


	def msg_to_all(self, msg, client):
		for c in self.clients:
			try:
				if c != client:
					c.send(msg)
			except:
				self.clients.remove(c)

	def aceptarCon(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				print("%s has connected", addr)
				conn.setblocking(False)
				self.clients.append(conn)
			except:
				pass

	def procesarCon(self):
		while True:
			if len(self.clients) > 0:
				for c in self.clients:
					try:
						data = c.recv(1024)
						if data:
							self.msg_to_all(data,c)
					except:
						pass


s = Server()