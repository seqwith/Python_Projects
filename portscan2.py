import pyfiglet
import socket
import sys
import argparse
from datetime import datetime
from threading import Thread, Lock
from queue import Queue

THREADS = 200

q = Queue()
print_lock = Lock()

def port_scan(port):

    #Scan a port on host

    try:
        s = socket.socket()
        s.connect((host, port))
    except:
        with print_lock:
            print(f"{host:15}: {port:5} is closed", end='\r')
    else:
        with print_lock:
            print(f"{host:15}: {port:5} is open", end='\r')
    finally:
        s.close()

def scan_thread():
    global q
    while True:
        #get the port from the queue
        worker = q.get()
        # Scan that port number
        port_scan(worker)
        #tells the queue that the scanning for that port is complete
        q.task_done()

def main(host,  ports):
    global q

    for i in range(THREADS):
        #start each thread
        i = Thread(target=scan_thread)
        #when we set daemon to true, the thread will end when main thread ends
        i.daemon = True
        #start the daemon thread
        i.start()
    for worker in ports:
        # for each port, put that port into the queue
        #to start scanning
        q.put(worker)
    # Wait for the threads to finish
    q.join()

if __name__ == "__main__":
    #parse some input parameters
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("host", help="host to scan")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    args = parser.parse_args()
    host, port_range = args.host, args.port_range

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [ p for p in range(start_port, end_port)]

    main(host, ports)