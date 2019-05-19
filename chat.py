import sys
import os
import json
import uuid
from Queue import *

class Chat:
	def __init__(self):
		self.sessions={}
		self.users = {}
		self.users['messi']={ 'nama': 'Lionel Messi', 'negara': 'Argentina', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
		self.users['henderson']={ 'nama': 'Jordan Henderson', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
		self.users['lineker']={ 'nama': 'Gary Lineker', 'negara': 'Inggris', 'password': 'surabaya','incoming': {}, 'outgoing':{}}
	def proses(self,data):
		j=data.split(" ")
		try:
			command=j[0].strip()
			if (command=='auth'):
				username=j[1].strip()
				password=j[2].strip()
                                print "auth {}" . format(username)
				return self.autentikasi_user(username,password)
			elif (command=='send'):
				sessionid = j[1].strip()
				usernameto = j[2].strip()
                                message=""
                                for w in j[3:]:
                                    message="{} {}" . format(message,w)
				usernamefrom = self.sessions[sessionid]['username']
                                print "send message from {} to {}" . format(usernamefrom,usernameto)
				return self.send_message(sessionid,usernamefrom,usernameto,message)
                        elif (command=='inbox'):
                                sessionid = j[1].strip()
                                username = self.sessions[sessionid]['username']
                                print "inbox {}" . format(sessionid)
                                return self.get_inbox(username)
			elif(command=='logout'):
				sessionid = j[1]
				username = self.sessions[sessionid]['username']
				print "{} {}" . format(command, username)
				return self.logout(sessionid)
			elif(command=='creategroup'):
				sessionid = j[1]
				group_name = j[2]
				print"{} {}" . format(command, group_name)
				return self.create_group(group_name, sessionid)
			elif(command=='joingroup'):
				sessionid = j[1]
				group_token = j[2]
				print"{} {}" . format(command, group_token)
				return self.join_group(group_token, sessionid)
			else:
				return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
		except IndexError:
			return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}
	def autentikasi_user(self,username,password):
		if (username not in self.users):
			return { 'status': 'ERROR', 'message': 'User Tidak Ada' }
 		if (self.users[username]['password']!= password):
			return { 'status': 'ERROR', 'message': 'Password Salah' }
		tokenid = str(uuid.uuid4()) 
		self.sessions[tokenid]={ 'username': username, 'userdetail':self.users[username]}
		return { 'status': 'OK', 'tokenid': tokenid }
	def get_user(self,username):
		if (username not in self.users):
			return False
		return self.users[username]
	def send_message(self,sessionid,username_from,username_dest,message):
		if (sessionid not in self.sessions):
			return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
		s_fr = self.get_user(username_from)
		s_to = self.get_user(username_dest)
		
		if (s_fr==False or s_to==False):
			return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

		message = { 'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message }
		outqueue_sender = s_fr['outgoing']
		inqueue_receiver = s_to['incoming']
		try:	
			outqueue_sender[username_from].put(message)
		except KeyError:
			outqueue_sender[username_from]=Queue()
			outqueue_sender[username_from].put(message)
		try:
			inqueue_receiver[username_from].put(message)
		except KeyError:
			inqueue_receiver[username_from]=Queue()
			inqueue_receiver[username_from].put(message)
		return {'status': 'OK', 'message': 'Message Sent'}

	def get_inbox(self,username):
		s_fr = self.get_user(username)
		incoming = s_fr['incoming']
		msgs={}
		for users in incoming:
			msgs[users]=[]
			while not incoming[users].empty():
				msgs[users].append(s_fr['incoming'][users].get_nowait())
			
		return {'status': 'OK', 'messages': msgs}
	def logout(self, tokenid):
		self.sessions[tokenid]=None
		return { 'status': 'OK', 'message': 'Logout succeed' }
	def create_group(self, group_name, sessionid):
		while(True):
			group_token = str(uuid.uuid4())[:5]
			if group_token not in self.groups:
				break
		admin_name = self.sessions[sessionid]['username']
		self.groups[group_token] = {'group_name':group_name, 'group_token':group_token, 'admin':admin_name, 'incoming':[], 'users':[]}
		self.groups[group_token]['users'].append(admin_name)
		return {'status':'OK', 'messages': self.groups[group_token]}
	def join_group(self, group_token, sessionid):
		username = self.sessions[sessionid]['username']
		if(group_token not in self.groups):
			return {'status':'Err', 'message':'404 Group not found'}
		if username not in self.groups[group_token]['users']:
			self.groups[group_token]['users'].append(username)
			return {'status':'OK', 'message':'Group joined successfully'}
		return {'status':'Err', 'message':'You already joined group'}

if __name__=="__main__":
	j = Chat()
        sesi = j.proses("auth messi surabaya")
	print sesi
	sesi = j.autentikasi_user('messi','surabaya')
	#print sesi
	tokenid = sesi['tokenid']
	print j.proses("send {} henderson hello gimana kabarnya son " . format(tokenid))
	print j.send_message(tokenid,'messi','henderson','hello son')
	print j.send_message(tokenid,'henderson','messi','hello si')
	print j.send_message(tokenid,'lineker','messi','hello si dari lineker')


	print j.get_inbox('messi')
















