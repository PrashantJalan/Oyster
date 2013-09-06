import socket
from multiprocessing import Process, Queue, Value
import os
import sys
import time


def main():
	
	#Constants
	PORT = 5036
	ADDRESS = "localhost"
	MAX_COUNT1 = 2				#Change these to schedule the processes
	MAX_COUNT2 = 5
	MAX_COUNT3 = 3
	MAX_COUNT4 = 2
	q1 = Queue()				#Buffer queue for register
	q2 = Queue()				#Buffer queue for sharing
	q3 = Queue()				#Buffer queue for search
	qd = Queue()				#Buffer queue for closed clients
	cDict = {}					#Dictionary for storing the clients

	#Assigning server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((ADDRESS, PORT))
	server_socket.listen(5)

	sys.stdout.write("Server running...\n");

	#Starting the queue handling processes
	for i in range(MAX_COUNT1):
		qH = Process(target=q1Handler, args=(qd,q1,cDict))
		qH.start()
	for i in range(MAX_COUNT2):
		qH = Process(target=q2Handler, args=(qd,q2,cDict))
		qH.start()
	for i in range(MAX_COUNT3):
		qH = Process(target=q3Handler, args=(qd,q3,cDict))
		qH.start()
	
	#Connecting to new Clients
	#All the I/O operations are also done here
	KEY = 0													#Unique key identifier for each client
	count4 = Value('i', 0)
	while 1:
		#Checking for clients
		if count4.value < MAX_COUNT4:
			client_socket, address = server_socket.accept()
			try:
				PORT += 1
				KEY += 1
				cDict[str(KEY)]=[client_socket,address]
				client_socket.send(str(PORT))				#Sending port to make a server
				time.sleep(0.5)								#Time reqd. to send the above packet
				count4.value += 1
				clientHandler = Process(target=newClient, args=(client_socket,address,count4,qd,q1,q2,q3,KEY))
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



def q1Handler(qd,q1,cDict):
	#This process empties the queue, updates the data structures.
	while 1:
		KEY = q1.get()
		print cDict
		[client_socket, address] = cDict[KEY]
		try:
			client_socket.send("Let's begin the registration process!\n")
		except:
			sys.stdout.write(str(address)+" closed due to error.\n")
			qd.put(KEY)



def q2Handler(qd,q2,cDict):
	#This process empties the queue, updates the data structures.
	while 1:
		KEY = q2.get()
		[client_socket, address] = cDict[KEY]
		try:
			client_socket.send("Knowledge grows when shared!\n")
		except:
			sys.stdout.write(str(address)+" closed due to error.\n")
			qd.put(KEY)


def q3Handler(qd,q3,cDict):
	#This process empties the queue, updates the data structures.
	while 1:
		KEY = q3.get()
		[client_socket, address] = cDict[KEY]
		try:
			client_socket.send("Enter your search string:\n")
		except:
			sys.stdout.write(str(address)+" closed due to error.\n")
			qd.put(KEY)		


def newClient(client_socket,address,count4,qd,q1,q2,q3,KEY):
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
				count4.value = count4.value-1
		except:
			sys.stdout.write(str(address)+" closed due to error.\n")
			qd.put(str(KEY))
			flag = False
			count4.value = count4.value-1
		break

	if flag:
		sys.stdout.write(str(address)+" added to queue.\n")



if __name__=='__main__':
	main()
