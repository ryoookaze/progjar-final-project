import socket
import threading
import sys
import pickle

IPclient=sys.argv[1]
class Cliente():
	"""docstring for Cliente"""
	def __init__(self, host="localhost", port=4000):
		
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
				if data:
					print(pickle.loads(str(data)))
			except:
				pass

	def send_msg(self, msg):
		self.sock.send(pickle.dumps(str(IPclient)+" says "+str(msg)))


c = Cliente()