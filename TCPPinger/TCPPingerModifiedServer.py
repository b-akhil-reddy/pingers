import socket
import threading
from TCPPingerServer import connectionHandler
import signal
import sys
sys.path.append("..")
from utils.Exceptions import handleSigterm,SigTermException

signal.signal(signal.SIGTERM,handleSigterm)

# Creating server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("",11001))
# Listening for connection
print("Listening on port 11001")
serverSocket.listen()

# Look for a connection request
while True:
    try:
        # On receiving a connection request assign the connection to a separate thread
        conn, (clientaddr,clientport) = serverSocket.accept()
        print(f"connected to {clientaddr}:{clientport}")
        # Using the connection handler defined in TCPPingerServer
        th = threading.Thread(target=connectionHandler,args=(conn,clientaddr,clientport))
        th.start()
    except (KeyboardInterrupt,SigTermException) as e:
        if type(e)==KeyboardInterrupt:
            print(f"Received either SIGINT")
        else:
            print(f"Received either SIGTERM")
        break
# Closing server socket
print("Closing server socket")
serverSocket.close()
