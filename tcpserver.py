import socket
from multiprocessing import Process, Queue
import os
import sys
import time


def main():
	
	#Constants
	PORT = 5031
	ADDRESS = "localhost"
	MAX_CLIENT = 2
	q1 = Queue()				#Buffer queue for register
	q2 = Queue()				#Buffer queue for sharing
	q3 = Queue()				#Buffer queue for search
	qc = Queue()				#Buffer queue for count
	qd = Queue()				#Buffer queue for closed clients
	cDict = {}					#Dictionary for storing the clients

	#Assigning server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((ADDRESS, PORT))
	server_socket.listen(5)

	sys.stdout.write("Server running...\n");

	#Connecting to new Clients
	KEY = 0													#Unique key identifier for each client
	DELETED = 0												#No. of clients processed
	while 1:
		#Checking for clients
		if KEY-DELETED<MAX_CLIENT:
			client_socket, address = server_socket.accept()
			try:
				PORT += 1
				KEY += 1
				cDict[str(KEY)]=[client_socket,address]
				client_socket.send(str(PORT))				#Sending port to make a server
				time.sleep(0.05)							#Time reqd. to send the above packet
				clientHandler = Process(target=newClient, args=(client_socket,address,qd,q1,q2,q3,KEY))
				clientHandler.start()
			except:
				continue
		else:
			client_socket, address = server_socket.accept()
			client_socket.send('Q')
			client_socket.close()
		
		#Deleting closed clients
		while not qd.empty():
			temp = qd.get()
			del cDict[temp]
			DELETED += 1
			


def newClient(client_socket,address,qd,q1,q2,q3,KEY):
	#This function will take input from the client and accordingly
	#add it to its buffer queue
	tmp0 = ""
	flag = True
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
			data = client_socket.recv(8)
			if data=='1':
				q1.put(str(KEY))
			elif data=='2':
				q2.put(str(KEY))
			elif data=='3':
				q3.put(str(KEY))
			elif i<=3 and data!='Q':
				tmp0 = "\nNot a valid input. Let's try again...\n"
				continue
			else:
				client_socket.send('Q')
				client_socket.close()
				sys.stdout.write(str(address)+" closed.\n")
				qd.put(str(KEY))
				flag = False
		except:
			sys.stdout.write(str(address)+" closed due to error.\n")
			qd.put(str(KEY))
			flag = False
		break

	if flag:
		sys.stdout.write(str(address)+" added to queue.\n")



if __name__=='__main__':
	main()
