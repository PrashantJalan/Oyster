from multiprocessing import Process
import os

x = 0

def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):  # only available on Unix
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

def f(name):
	global x
	x += 1
	info('function f')
	print 'hello', name

def lol():
	global x
	x += 1
	info('main line')
	p = Process(target=f, args=('bob',))
	p.start()
	p.join()
	print x

if __name__ == '__main__':
	lol()

