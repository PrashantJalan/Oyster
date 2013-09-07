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
buf = Queue.Queue()						#Buffer queue for new clients
online = []								#Buffer queue for online clients
db = []									#Database


def main():
	global q1
	global q2
	global q3
	global buf
	global online
	MAX_COUNT1 = 10						#Change these for diff scheduling algorithms
	MAX_COUNT2 = 5
	MAX_COUNT3 = 3
	MAX_COUNT4 = 3
	PORT = 5680
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
	for i in range(MAX_COUNT4):
		threading.Thread(target = newClient, args = ()).start()
		
	while 1:
		#Checking for clients
		client_socket, address = server_socket.accept()
		try:
			PORT += 1
			client_socket.send(str(PORT))				#Sending port to make a server
			time.sleep(0.1)								#Time reqd. to send the above packet
			buf.put([client_socket, address, PORT])
			online.append([client_socket, address, PORT])
		except:
			continue
		

def q1Handler():
	#This process empties the queue, updates the data structures.
	global q1
	global q2
	global q3
	global buf

	while 1:
		[client_socket, address, PORT] = q1.get()
		try:
			client_socket.send("Let's begin the registration process!\nEnter your full name:")
			data = client_socket.recv(512)
			client_socket.send("Enter your email address:")
			data = client_socket.recv(512)
			client_socket.send("\recYou are now registered to our network!\n")
			buf.put([client_socket, address, PORT])
		except:
			pass


def q2Handler():
	#This process empties the queue, updates the data structures.
	global q1
	global q2
	global q3
	global db
	global buf

	while 1:
		[client_socket, address, PORT] = q2.get()
		try:
			client_socket.send("Knowledge grows with sharing!\nEnter your no. of files you want to share:")
			data = client_socket.recv(8)
			for i in range(int(data)):
				client_socket.send("Enter the full file path:")
				data = client_socket.recv(512)
				db.append([data, [client_socket, address, PORT]])
			client_socket.send("\recThank you for sharing!\n")
			buf.put([client_socket, address, PORT])
		except:
			buf.put([client_socket, address, PORT])
			
			
def q3Handler():
	#This process empties the queue, updates the data structures.
	global q1
	global q2
	global q3
	global db
	global buf
	global online

	while 1:
		[client_socket, address, PORT] = q3.get()
		try:
			client_socket.send("Enter the search string: (* for all)")
			data = client_socket.recv(512)
			tmp = []
			i = 0
			result = ""
			if data == '*':
				for it in db:
					result = result+str(i+1)+": "+it[0]+'\n'
					tmp.append(str(it[1][2])+" "+it[0])
					i = i+1
			else:
				for it in db:
					if data in it[0]:
						if it[1] in online:
							result = result+str(i+1)+": "+it[0]+'\n'
							tmp.append(str(it[1][2])+" "+it[0])
							i = i+1
			if i==0:
				client_socket.send("\recSorry! No files found.\n")
			else:
				result += "Enter the file number: (-1 if you don't want to download)"
				client_socket.send(result)
				data = client_socket.recv(8)
				if data!='-1':
					client_socket.send("dl"+tmp[int(data)-1])
				else:
					client_socket.send("\rec\n")
			buf.put([client_socket, address, PORT])
		except:
			buf.put([client_socket, address, PORT])		


def newClient():
	#This function will take input from the client and accordingly
	#add it to its buffer queue
	global q1
	global q2
	global q3
	global buf
	global online
	tmp0 = ""

	while 1:
		[client_socket, address, PORT] = buf.get()
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
					q1.put([client_socket,address,PORT])
				elif data=='2':
					q2.put([client_socket,address,PORT])						
				elif data=='3':
					q3.put([client_socket,address,PORT])						
				elif i<=3 and data!='Q':
					tmp0 = "\nNot a valid input. Let's try again...\n"
					continue
				else:
					client_socket.send('Q')
					client_socket.close()
					online.remove([client_socket, address, PORT])
					sys.stdout.write(str(address)+" closed.\n")
			except:
				online.remove([client_socket, address, PORT])
				sys.stdout.write(str(address)+" closed due to error.\n")
			break



if __name__=='__main__':
	main()
