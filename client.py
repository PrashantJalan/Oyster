import socket
import sys
import threading


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
	global server_socket
	global client_socket
	
	#Constants		
	PORT = 5680
	ADDRESS = "localhost"

	client_socket.connect((ADDRESS, PORT))

	#Making the client a server
	data = client_socket.recv(8)
	if data=='Q':
		print "Connection to server closed."
		client_socket.close()
		quit()
	else:
		NEW_PORT = int(data)
	
	server_socket.bind((ADDRESS, NEW_PORT))
	server_socket.listen(5)
	sys.stdout.write("Made the client a server on PORT "+str(NEW_PORT)+'\n')

	#Starting threads
	threading.Thread(target = clientFunc, args = ()).start()
	t = threading.Thread(target = serverFunc, args = ())
	t.daemon = True
	t.start()
	

def serverFunc():
	global server_socket
	
	while 1:
		#Checking for clients
		client_socket2, address = server_socket.accept()
		try:
			f = client_socket2.recv(512)
			print f
		except:
			continue


def clientFunc():
	global client_socket
	
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
			DL_PORT = int(data[2:].split()[0])
			FILE = data[2:].split()[1]
			print DL_PORT, FILE
			print "Establishing a p2p connection..."
			try:
				peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				peer_socket.connect((ADDRESS, DL_PORT))
				print "Connection Established"
				peer_socket.send(FILE)
			except:
				print "Some error occured! Could not download"
			continue		
		print data
		data = raw_input()
		client_socket.send(data)


if __name__=='__main__':
	main()
