__author__ = 'Melody'

from socket import *

hostName = 'www.google.com'
port = 80
clientSocket = create_connection((hostName, port))    #use create_connection to create a TCP socket because hostName can be non-numeric 
print 'Connection established'

data = 'GET /index.html HTTP/1.1\r\nHost: www-net.cs.umass.edu\r\nUser-Agent: Firefox/3.6.10\r\nAccept: text/html,application/xhtml+xml\r\nAccept-Language: en-us,en;q=0.5\r\nAccept-Encoding: gzip,deflate\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7\r\nKeep-Alive: 115\r\nConnection: keep-alive\r\n\r\n'
clientSocket.send(data)

while 1:
        response = clientSocket.recv(1024)
        print response

clientSocket.close() #closes socket, therefore closing TCP connection btwn client and server