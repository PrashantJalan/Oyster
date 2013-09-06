# TCP server example

import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5000))
server_socket.listen(5)

print "Server running..."
print "TCPServer Waiting for client on port 5000"

while 1:
	client_socket, address = server_socket.accept()
	print "I got a connection from ", address
	if os.fork()==0:
		while 1:
			print "Welcome Guest!"
			print "Select an option from the list - "
			print "1: Register with Oyster"
			print "2: Share a file"
			print "3: Search for a file"
			print "Q: Quit"
				 
			data = client_socket.recv(1)
			print data
			if (data == 'Q'):
				client_socket.close()
				break;
			
