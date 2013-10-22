#!/usr/bin/env python

"""
    proxy.py: a simple multi-threaded web proxy
    - Assumes client input is always valid or correct.
    - Handles HTTP/1.1 and HTTP/1.0, GET, CONNECT

    Sze Yan Li
    CIS432
    Assignment 1: Multi-Threaded Web Proxy
"""
__author__      = "Sze Yan Li"
__date__        = "10/16/2013"

import socket
import threading
import re
import sys
import logging
import time

# ##########################################

# ------ CONSTANTS
RECV_SIZE = 4096    #buffer size of recv
MAX_Q = 200   #max number of connect requests to queue before refusing outside connections

# ------ MAIN PROGRAM
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(threadName)s %(message)s', )

def main():
    #host and port
    host = ''       #blank is default for localhost
    port = 22591

    #make a socket and bind to host and port
    mainSocket = None
    try:
        mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mainSocket.bind((host, port))
        mainSocket.listen(MAX_Q)

    except socket.error, (message):
        if mainSocket:
            mainSocket.close()
        print 'Error:', message
        sys.exit(1)
    print 'The proxy is ready to receive\n'

    #Wait until request arrives.  Create a thread and dedicated socket for each HTTP request.
    while 1:
        clientSocket, clientAddress = mainSocket.accept()
        t = threading.Thread(target=proxy_thread, args=(clientSocket, clientAddress))
        t.start()

    mainSocket.close()

# ------ PROXY THREAD
def proxy_thread(clientSocket, clientAddress):
    logging.debug('Starting')

    #get HTTP request
    request = clientSocket.recv(RECV_SIZE)

    #extract port (if necessary) and host name from HTTP request
    hostName = ''
    port = 80
    for line in request.split('\n'):
        if line[0:4] == 'CONN': #CONNECT method has special port
            s = re.split(' |:', line)   #split by white space and colon
            port = s[2] #should be 3rd element if there is a port
            port = port.strip()

        if line[0:4] == 'Host' or line[0:4] == 'From':
            hostName = line.split(' ')[1]   #grab the host name
            hostName = hostName.strip()
            break

    #create a socket, connect, and send request to server
    serverSocket = None
    try:
        serverSocket = socket.create_connection((hostName, port))    #use create_connection to create a TCP socket because hostName can be non-numeric
        serverSocket.sendall(request)

        content_length = RECV_SIZE + 1 #one bigger than the possible RECV_SIZE (place-holder for first while loop)
        content_bool = 0    #flag for if Content-Length was found
        recv_thusfar = 0    #bytes received thus far

        #set time out as an extra pre-caution
        serverSocket.settimeout(30)
        clientSocket.settimeout(30)

        #wait and receive response. Then send response back to client
        while 1:
            response = serverSocket.recv(RECV_SIZE)
            recv_thusfar = recv_thusfar + len(response)

            #parse real content length in first loop
            if(content_length == RECV_SIZE + 1):
                for line in response.split('\n'):
                    if line[0:14] == 'Content-Length':
                        #find and set content_length
                        content_length = line.split(' ')[1]   #grab the content length
                        content_length = int(content_length.strip())

                        content_bool = 1    #set found flag to true
                        recv_thusfar = len(response.split('\r\n\r\n')[1])    #chop off headers to get content only

                        break
            if(content_bool):   #content length was found
                clientSocket.send(response)
                if(recv_thusfar >= content_length):
                    break
            else:
                if(len(response.strip()) > 0):
                    clientSocket.sendall(response)
                else:   #if there is no more data, then break out of while-loop
                    break

        #close sockets
        serverSocket.close()
        clientSocket.close()
        #close thread
        logging.debug('Ending Normally')
    except socket.error, (message):
        if serverSocket:
            serverSocket.close()
        if clientSocket:
            clientSocket.close()
        s = 'Ending -- Error:', message
        logging.debug(s)
        sys.exit(1)

# -------
if __name__ == '__main__':
    main()