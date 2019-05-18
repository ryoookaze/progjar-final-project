import socket
import os
import select
import json
import sys
import pickle
import threading

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889


class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP,TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid=""

        groupmessage = threading.Thread(target=self.groupmessage)

        groupmessage.daemon = True
        groupmessage.start()

    def proses(self,cmdline):
	j=cmdline.split(" ")
	try:
	    command=j[0].strip()
	    if (command=='auth'):
		username=j[1].strip()
		password=j[2].strip()
		return self.login(username,password)
	    elif (command=='send'):
		usernameto = j[1].strip()
                message=""
                for w in j[2:]:
                   message="{} {}" . format(message,w)
		return self.sendmessage(usernameto,message)
            elif (command=='inbox'):
                return self.inbox()
            elif(command=='logout'):
                tokenid = ''
                return self.logout()
            elif(command=='groupchat'):
                username = j[3].strip()
                return self.groupmessage(username)
	    else:
		return "*Maaf, command tidak benar"
	except IndexError:
	    return "-Maaf, command tidak benar"
    def sendstring(self,string):
        try:
            self.sock.sendall(string)
            receivemsg = ""
            while True:
                data = self.sock.recv(10)
                if (data):
                    receivemsg = "{}{}" . format(receivemsg,data)
                    if receivemsg[-4:]=="\r\n\r\n":
                        return json.loads(receivemsg)
        except:
            self.sock.close()
    def login(self,username,password):
        string="auth {} {} \r\n" . format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=result['tokenid']
            return "username {} logged in, token {} " .format(username,self.tokenid)
        else:
            return "Error, {}" . format(result['message'])
    def logout(self, username):
        return "username {} logged out" . format(username)
    def sendmessage(self,usernameto="xxx",message="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="send {} {} {} \r\n" . format(self.tokenid,usernameto,message)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "message sent to {}" . format(usernameto)
        else:
            return "Error, {}" . format(result['message'])
    def inbox(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="inbox {} \r\n" . format(self.tokenid)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])
    def sendgroupchat(self,msg):
        self.sock.send(pickle.dumps(msg))
    def groupmessage(self,username):
        if(self.tokenid==""):
            return "Error, not authorized"
        while True:
            msg = input('->')
            if (msg != ' out'):
                self.sendgroupchat(msg)
        while True:
			try:
				data = self.sock.recv(1024)
				if data:
					print(pickle.loads(data))
			except:
				pass



if __name__=="__main__":
    cc = ChatClient()
    while True:
        cmdline = raw_input("Command {}:" . format(cc.tokenid))
        print cc.proses(cmdline)

