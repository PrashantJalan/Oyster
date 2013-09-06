
import threading
import time

# Define a function for the thread
def print_time( threadName):
   global delay
   count = 0
   while 1:
      time.sleep(delay)
      count += 1
      print count

# Create two threads as follows
delay=2
threading.Thread( target=print_time, args= ("Thread-1",) ).start()

time.sleep(10)
delay +=2
