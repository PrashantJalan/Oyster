import socket
import sys


def main():
	#Constants		
	PORT = 5585
	ADDRESS = "localhost"

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((ADDRESS, PORT))

	#Making the client a server
	data = client_socket.recv(8)
	if data=='Q':
		print "Connection to server closed."
		client_socket.close()
		quit()
	else:
		NEW_PORT = int(data)
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((ADDRESS, NEW_PORT))
	server_socket.listen(5)
	sys.stdout.write("Made the client a server on PORT "+str(NEW_PORT)+'\n')

	while 1:
		data = client_socket.recv(512)
		if '\rec' in data[0:4]:
			print data[3:]
			continue
		if data=='Q':
			print "Connection to server closed."
			client_socket.close()
			quit()
		if data[0:2]=='dl':
			DL_PORT = data[2:].split()[0]
			FILE = data[2:].split()[1]
			print DL_PORT, FILE
			continue		
		print data
		data = raw_input()
		client_socket.send(data)


if __name__=='__main__':
	main()
