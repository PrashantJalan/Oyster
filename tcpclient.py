# TCP client example

import socket

PORT = 5007
ADDRESS = "localhost"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ADDRESS, PORT))

#Making the client a server
HOST = client_socket.recv(512)
PORT2 = client_socket.recv(512)
print HOST
print int(PORT2)
client_socket.bind((HOST, int(PORT2)))
client_socket.listen(5)

while 1:
	data = client_socket.recv(512)
	print data
	data = raw_input()
	
	if (data <> 'Q'):
		client_socket.send(data)
	else:
		client_socket.send(data)
		client_socket.close()
		break;

