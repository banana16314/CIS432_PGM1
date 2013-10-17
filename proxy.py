#!/usr/bin/env python

"""
    proxy.py: a bare-bones, multi-threaded web proxy with no exception handling or error checking.  
    - Assumes client input is always valid or correct.
    - Assumes host is always 2nd line of HTTP request message

    Sze Yan Li
    CIS432
    Assignment 1: Multi-Threaded Web Proxy
"""
__author__      = "Sze Yan Li"
__date__        = "10/16/2013"

import socket
import thread
import os

# ##########################################

# ------ CONSTANTS    
RECV_SIZE = 1024   #buffer size of recv
 
# ------ MAIN PROGRAM
def main():

    #host and port
    host = ''       #TODO set to ix.cs.uoregon.edu? set blank for localhost.  
    port = 22591
    
    #make a socket and bind to host and port  #socket.error, msg
    mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    mainSocket.bind((host, port))  
    mainSocket.listen(25)   #max of 25 connect requests to queue before refusing outside connections
    print 'The proxy is ready to receive\n'
    
    #Wait until request arrives.  Create a thread and dedicated socket for each HTTP request.
    while 1:   
        clientSocket, clientAddress = mainSocket.accept()  
        thread.start_new_thread(proxy_thread, (clientSocket, clientAddress))
        
    mainSocket.close()

# ------ PROXY THREAD
def proxy_thread(clientSocket, clientAddress):
    
    #get HTTP request
    request = clientSocket.recv(RECV_SIZE)
    print request
    
    #get server and port from HTTP request
    getLine = request.split(os.linesep)[1]    #2nd line contains server (and port).
    #print getLine
    
    hostName = getLine.split(' ')[1]   #grab the host name. ie: www.google.com
    hostName = hostName.strip()
    hostAddress = socket.gethostbyname(hostName)
    print hostName, hostAddress
    
    port = 80    #set default port
    s = hostName.split(':') 
    if len(s) > 1:    #TODO test this. array should contain 2 elements if there is a special port specified
        port = s[1]
        port = port.strip()
    #print port
    
    #create a socket, connect, and send request to server 
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((hostAddress, port))
    #serverSocket = socket.create_connection((hostName, port))    #use create_connection to create a TCP socket because hostName can be non-numeric  
    print 'Re-directing request to: ',hostName, hostAddress
    serverSocket.send(request)

    #receive and send response back to client
    response = serverSocket.recv(RECV_SIZE)
    clientSocket.send(response)
    print 'Sent request to client'
    
    #close sockets
    serverSocket.close()
    clientSocket.close()
    print 'done'

# -------
if __name__ == '__main__':
    main()
