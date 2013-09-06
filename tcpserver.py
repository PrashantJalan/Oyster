# TCP server example

import socket
import os
import sys

PORT = 5005
ADDRESS = ""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ADDRESS, PORT))
server_socket.listen(5)

sys.stdout.write("Server running...\n");

while 1:
	client_socket, address = server_socket.accept()
	if os.fork()==0:
		sys.stdout.write("I got a connection from "+str(address)+"\n")
		STATE = 'INITIAL'
		while 1:
			if STATE=='INITIAL':
				tmp1 = "Welcome Guest!\n"
				tmp2 = "Select an option from the list -\n"
				tmp3 = "1: Register with Oyster\n"
				tmp4 = "2: Share a file\n"
				tmp5 = "3: Search for a file\n"
				tmp6 = "Q: Quit\n"
				data = tmp1+tmp2+tmp3+tmp4+tmp5+tmp6
			
			client_socket.send(data)
							 
			data = client_socket.recv(512)
			sys.stdout.write("Received data from "+str(address)+": "+data+"\n")
			if (data == 'Q'):
				client_socket.close()
				sys.stdout.write(str(address)+" closed.\n")
				quit()
