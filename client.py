import socket
import threading
import sys
import pickle

class Client():

	def __init__(self, host="0.0.0.0", port=4000):
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((str(host), int(port)))
		msg_recv = threading.Thread(target=self.msg_recv)

		msg_recv.daemon = True
		msg_recv.start()

		while True:
			msg = input('->')
			if msg != 'out':
				self.send_msg(msg)
			else:
				self.sock.close()
				sys.exit()

	def msg_recv(self):
		while True:
			try:
				data = self.sock.recv(1024)
				hostname = socket.gethostname()
				ipaddr = socket.gethostname(hostname)
				if data:
					print(ipaddr + pickle.loads(data))
			except:
				pass

	def send_msg(self, msg):
		init = self.sock.send(pickle.dumps(msg))


c = Client()