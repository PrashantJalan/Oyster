import socket
import os
import sys
import time


#Constants
PORT = 5010
ADDRESS = ""
tmp1 = "Welcome Guest!\n"
tmp2 = "Select an option from the list -\n"
tmp3 = "1: Register with Oyster\n"
tmp4 = "2: Share a file\n"
tmp5 = "3: Search for a file\n"
tmp6 = "Q: Quit\n"


#Assigning server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ADDRESS, PORT))
server_socket.listen(5)

sys.stdout.write("Server running...\n");


#Connecting to new Clients
while 1:
	client_socket, address = server_socket.accept()
	PORT += 1
	if os.fork()==0:
		try:
		
		except:
			sys.stdout.write(str(address)+" closed due to error.\n")
			quit()
