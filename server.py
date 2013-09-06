import socket
import threading
import os
import sys
import Queue
import time

#Constants
q1 = Queue.Queue()						#Buffer queue for register
q2 = Queue.Queue()						#Buffer queue for sharing
q3 = Queue.Queue()						#Buffer queue for search
c4 = 0									#Count; needed for checking new clients


def main():
	global q1
	global q2
	global q3
	global c4
	MAX_COUNT1 = 10						#Change these for diff scheduling algorithms
	MAX_COUNT2 = 5
	MAX_COUNT3 = 3
	MAX_COUNT4 = 3
	PORT = 5535
	ADDRESS = "localhost"
	
	#Assigning server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((ADDRESS, PORT))
	server_socket.listen(5)

	sys.stdout.write("Server running...\n");
	
	#Starting the threads
	for i in range(MAX_COUNT1):
		threading.Thread(target = q1Handler, args = ()).start()
	for i in range(MAX_COUNT2):
		threading.Thread(target = q2Handler, args = ()).start()
	for i in range(MAX_COUNT3):
		threading.Thread(target = q3Handler, args = ()).start()

	while 1:
		#Checking for clients
		if c4 <= MAX_COUNT4:
			client_socket, address = server_socket.accept()
			try:
				PORT += 1
				client_socket.send(str(PORT))				#Sending port to make a server
				time.sleep(0.1)								#Time reqd. to send the above packet
				c4 += 1
				threading.Thread(target = newClient, args = (client_socket, address)).start()
			except:
				continue
		else:
			client_socket, address = server_socket.accept()
			client_socket.send('Q')
			client_socket.close()


def q1Handler():
	#This process empties the queue, updates the data structures.
	global q1
	global q2
	global q3

	while 1:
		[client_socket, address] = q1.get()
		try:
			client_socket.send("Let's begin the registration process!\nEnter your full name:")
			data = client_socket.recv(512)
			client_socket.send("Enter your email address:")
			data = client_socket.recv(512)
			client_socket.send("You are now registered to our network!\nQ")
			client_socket.close()
			sys.stdout.write(str(address)+" closed.\n")
		except:
			pass


def q2Handler():
	#This process empties the queue, updates the data structures.
	global q1
	global q2
	global q3

	while 1:
		[client_socket, address] = q2.get()
		try:
			client_socket.send("Knowledge grows with sharing!\nEnter your no. of files you want to share:")
			data = client_socket.recv(8)
			for i in range(int(data)):
				client_socket.send("Enter the full file path:")
				data = client_socket.recv(512)
			client_socket.send("Thank you for sharing!\nQ")
			client_socket.close()
			sys.stdout.write(str(address)+" closed.\n")
		except:
			pass
			
			
def q3Handler():
	#This process empties the queue, updates the data structures.
	global q1
	global q2
	global q3

	while 1:
		[client_socket, address] = q3.get()
		try:
			client_socket.send("Enter the search string:")
			data = client_socket.recv(512)
			client_socket.close()
			sys.stdout.write(str(address)+" closed.\n")
		except:
			pass			


def newClient(client_socket, address):
	#This function will take input from the client and accordingly
	#add it to its buffer queue
	global q1
	global q2
	global q3
	global c4
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
				q1.put([client_socket,address])
			elif data=='2':
				q2.put([client_socket,address])						
			elif data=='3':
				q3.put([client_socket,address])						
			elif i<=3 and data!='Q':
				tmp0 = "\nNot a valid input. Let's try again...\n"
				continue
			else:
				client_socket.send('Q')
				client_socket.close()
				sys.stdout.write(str(address)+" closed.\n")
				flag = False
				c4 -= 1
		except:
			sys.stdout.write(str(address)+" closed due to error.\n")
			flag = False
			c4 -= 1
		break

	if flag:
		sys.stdout.write(str(address)+" added to queue.\n")



if __name__=='__main__':
	main()
