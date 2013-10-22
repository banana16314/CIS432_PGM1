#!/usr/bin/env python

"""
    proxy.py: a bare-bones, multi-threaded web proxy with minimal exception handling and error checking.  
    - Assumes client input is always valid or correct.
    - Handles HTTP/1.1 and HTTP/1.0, GET, CONNECT

    Sze Yan Li
    CIS432
    Assignment 1: Multi-Threaded Web Proxy
"""
__author__      = "Sze Yan Li"
__date__        = "10/16/2013"

import socket
import thread
import re
import sys

# ##########################################

# ------ CONSTANTS    
RECV_SIZE = 4096    #buffer size of recv
MAX_Q = 200   #max number of connect requests to queue before refusing outside connections
  
# ------ MAIN PROGRAM
def main():

    #host and port
    host = ''       #blank is default for localhost  
    port = 22591
    
    #make a socket and bind to host and port
    try:      
        mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        mainSocket.bind((host, port))  
        mainSocket.listen(MAX_Q)   
        
    except socket.error, (value, message):  
        if mainSocket:
            mainSocket.close()
        print 'Error:', message
        sys.exit(1)      
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
    #print request
    
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
    try:
        serverSocket = socket.create_connection((hostName, port))    #use create_connection to create a TCP socket because hostName can be non-numeric  
        serverSocket.sendall(request)
        
        content_length = RECV_SIZE + 1 #one bigger than the possible RECV_SIZE (place-holder for first while loop)
        recv_thusfar = 0    #bytes received thus far
        
        #wait and receive response. Then send response back to client
        while 1:    #while there is still data to send
            response = serverSocket.recv(RECV_SIZE)
            recv_thusfar = recv_thusfar + len(response)

            if(content_length == RECV_SIZE + 1):
                #parse real content length
                for line in response.split('\n'):    
                    if line[0:14] == 'Content-Length':
                        content_length = line.split(' ')[1]   #grab the content length
                        content_length = content_length.strip()                        
                        break
            if(len(response) > 0 or recv_thusfar >= content_length):
                clientSocket.sendall(response)
            else:
                break      
                
        #close sockets
        serverSocket.close()
        clientSocket.close()      
    except socket.error, (value, message):  
        if serverSocket:
            serverSocket.close() 
        if clientSocket:
            clientSocket.close() 
        print 'Error:', message
        sys.exit(1)
        
# -------
if __name__ == '__main__':
    main()
