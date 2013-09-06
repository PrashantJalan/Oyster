import socket

PORT = 5010
ADDRESS = "localhost"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ADDRESS, PORT))

#Making the client a server
NEW_PORT = int(client_socket.recv(8))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ADDRESS, NEW_PORT))
server_socket.listen(5)

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

