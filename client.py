import socket
import sys
import threading
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
	global server_socket
	global client_socket
	
	#Constants		
	PORT = 5900
	ADDRESS = "localhost"
	CHUNK_SIZE = 1024

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
	sys.stdout.write("\nMade the client a server on PORT "+str(NEW_PORT)+'\n\n')

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
			try:
				content = open(f).read()
				length = len(content)
				client_socket2.send(str(length))
				time.sleep(0.1)
				for it in content:
					client_socket2.send(it)
				client_socket2.close()	
			except:
				client_socket2.send('X')
				client_socket2.close()			
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
			tmp = data[2:].split()
			DL_ADRS = tmp[0][2:-2]
			DL_PORT = int(tmp[3])
			FILE = tmp[2]
			print DL_ADRS, DL_PORT, FILE
			print "Establishing a p2p connection..."
			try:
				peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				peer_socket.connect((DL_ADRS, DL_PORT))
				print "Connection Established"
				peer_socket.send(FILE)
				tmp = peer_socket.recv(512)
				if tmp=='X':
					print "Some error occured! File not found problem.\n"
					peer_socket.close()
					continue
				else:
					length = int(tmp)
				print "Length of the file - ",length,". Downloading..."
				tmp = peer_socket.recv(1)
				if tmp=='X':
					print "Some error occured! Transfer of bytes problem.\n"
					peer_socket.close()
					continue
				else:
					content = tmp
				for i in range(length-1):
					tmp = peer_socket.recv(1)
					content += tmp
				f = open("/home/prashant/Downloads/"+FILE.split('/')[-1], 'w')
				f.write(content)
				f.close()
				print "File Dowloaded successfully."
				sys.stdout.write("File saved to "+"/home/prashant/Downloads/"+FILE.split('/')[-1]+'\n\n')
				peer_socket.close()
			except:
				print "Some error occured! Could not download\n"
			continue		
		print data
		data = raw_input()
		client_socket.send(data)


if __name__=='__main__':
	main()
