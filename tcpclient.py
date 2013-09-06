import socket
import sys



def main():
	
	#Constants		
	PORT = 5160
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
		if data=='Q':
			print "Connection to server closed."
			client_socket.close()
			quit()
		
		print data
		data = raw_input()
		client_socket.send(data)



if __name__=='__main__':
	main()
