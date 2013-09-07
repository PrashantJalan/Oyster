Oyster
======

This is done as a part of the first assignment of the Networks course on socket programming. It is a server-client as well as p2p implementation. 

The implementation is designed to work on the same computer. However, it can word on different computers as well. Just the PORT needs to be made static. 

First, multiprocessing was used instead of threading or thread module in python because it makes better use of the computational resources of multi-core machines. It creates child processes instead of threads. But it creates lots of problem when we need to use shared memory. Therefore, later multithreading was used.

The server.py and client.py are the fully working programs. The tcpserver.py and tcpclient.py are undeveloped programs using multiprocessing.

The programs use socket programming for communication as well as file transferring.

Buffer queue are used for shared communication between threads. It is implemented using the Queue module in python.

Changing the MAX_COUNT1, MAX_COUNT2, MAX_COUNT3, MAX_COUNT4 changes the scheduling between the different processes.

References
==========

http://effbot.org/zone/
http://www.tutorialspoint.com/python/python_networking.htm
http://effbot.org/zone/asyncore-ftp-client.htm
http://pymotw.com/2/socket/tcp.html
http://docs.python.org/2/library/multiprocessing.html
http://docs.python.org/2/library/threading.html
http://docs.python.org/2/library/socket.html
http://docs.python.org/2/library/queue.html
