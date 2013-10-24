# ################################
# Multi-Threaded Web Proxy
# CIS432
# ################################

AUTHOR
    Sze Yan Li

DESCRIPTION
    A simple multi-threaded web proxy
    
    - Assumes client input is always valid or correct.
    - Handles HTTP/1.1 and HTTP/1.0, GET, CONNECT
    - Debug shows opening and closing threads
    
    * Tested on IX on Firefox, Google Chrome.  Confirmed working for:
        - cs.uoregon.edu
        - spur.uoregon.edu
        - ix.cs.uoregon.edu
        - cnn.com
        - ebay.com
        - etc

THANKS/CREDITS
    Python documentation
        - http://docs.python.org/2/howto/sockets.html
        
    Python tutorial on socket exceptions
        - http://ilab.cs.byu.edu/python/socket/exceptions.html
    
    Python tutorial on threading
        - http://www.tutorialspoint.com/python/python_multithreading.htm
        
    Python tutorial on web proxies
        - http://luugiathuy.com/2011/03/simple-web-proxy-python/

RELEVANT FILES
    'proxy.py'  - contains web proxy program
	
SETUP
    Set up your proxy settings in the browser with the following:
        - default host: localhost
        - default port: 22591
    
    * to change any of the above, please edit directly in the code
    
BUILD/RUN
	'make'		- to run proxy.py.  Can also type: 'python proxy.py'


