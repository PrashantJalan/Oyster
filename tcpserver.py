import socket
from multiprocessing import Process, Queue
import os
import sys
import time


def main():
	
	#Constants
	PORT = 5020
	ADDRESS = "localhost"
	MAX_CLIENT = 2
	q1 = Queue()				#Buffer queue for register
	q2 = Queue()				#Buffer queue for sharing
	q3 = Queue()				#Buffer queue for search
	qc = Queue()				#Buffer queue for count

	#Assigning server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((ADDRESS, PORT))
	server_socket.listen(5)

	sys.stdout.write("Server running...\n");

	#Connecting to new Clients
	while 1:
		if qc.qsize()<MAX_CLIENT:
			client_socket, address = server_socket.accept()
			PORT += 1
			client_socket.send(str(PORT))				#Sending port to make a server
			time.sleep(0.05)							#Time reqd. to send the above packet
			qc.put('X')									#Maintaining the no. of processes
			clientHandler = Process(target=newClient, args=(client_socket,address,qc,q1,q2,q3))
			clientHandler.start()
		else:
			client_socket, address = server_socket.accept()
			client_socket.send('Q')
			client_socket.close()



def newClient(client_socket,address,qc,q1,q2,q3):
	tmp0 = ""
	sys.stdout.write("Got a connection from "+str(address)+'\n')
	i = 0
	while 1:
		i += 1
		try:
			tmp1 = "Welcome Guest!\n"
			tmp2 = "Select an option from the list -\n"
			tmp3 = "1: Register with Oyster\n"
			tmp4 = "2: Share a file\n"
			tmp5 = "3: Search for a file\n"
			tmp6 = "Q: Quit\n"
			client_socket.send(tmp0+tmp1+tmp2+tmp3+tmp4+tmp5+tmp6)
			data = client_socket.recv(1)
			if data=='1':
				q1.put('X')
			elif data=='2':
				q2.put('X')
			elif data=='3':
				q3.put('X')
			elif data!='Q' and i<=3:
				tmp0 = "\nNot a valid input. Let's try again...\n"
				continue
			client_socket.send('Q')
			client_socket.close()
			sys.stdout.write(str(address)+" closed.\n")
			qc.get()
			break
		except:
			sys.stdout.write(str(address)+" closed due to error.\n")
			qc.get()
			break
		


if __name__=='__main__':
	main()
