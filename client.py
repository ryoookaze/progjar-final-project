import socket
import threading
import sys
import uuid
import pickle

IPclient=sys.argv[1]
class Cliente():
	def __init__(self, host="localhost", port=4000):
		self.sessions={}
		self.users = {}
		self.users['messi']={ 'nama': 'Lionel Messi', 'negara': 'Argentina', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
		self.users['henderson']={ 'nama': 'Jordan Henderson', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
		self.users['lineker']={ 'nama': 'Gary Lineker', 'negara': 'Inggris', 'password': 'surabaya','incoming': {}, 'outgoing':{}}
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((str(host), int(port)))

		msg_recv = threading.Thread(target=self.msg_recv)

		msg_recv.daemon = True
		msg_recv.start()

		while True:
			msg = input('->')
			if msg != "{quit}":
				self.send_msg(msg)
			else:
				self.sock.close()
				sys.exit()
	def progress(self, data):
		try:
			command = input('->')
			if (command == 'auth'):
				username=j[1].strip()
				password=j[2].strip()
				print("auth {}" . format(username))
				return self.user_authentication(username, password)

	def user_authentication(self, username, password):
		if (username not in self.users):
			return { 'status': 'ERROR', 'message': 'User Tidak Ada' }
 		if (self.users[username]['password']!= password):
			return { 'status': 'ERROR', 'message': 'Password Salah' }
		tokenid = str(uuid.uuid4()) 
		self.sessions[tokenid]={ 'username': username, 'userdetail':self.users[username]}
		return { 'status': 'OK', 'tokenid': tokenid }
		
	def msg_recv(self):
		while True:
			try:
				data = self.sock.recv(1024)
				if data:
					print(str(pickle.loads(data)))
			except:
				pass

	def send_msg(self, msg):
		self.sock.send(bytes(msg, "utf-8"))

c = Cliente()