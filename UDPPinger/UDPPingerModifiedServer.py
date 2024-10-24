### Following command was used to simulate the loss on loopback interface
# sudo tc qdisc add dev <interface> root netem loss <percentage>

### Following code is same as that in UDPPingerServer.py
# The only modification done here is by removing lines that are used to
# simulate packetloss


# We will need the following module to generate randomized lost packets
from socket import *
import sys
import signal
import threading

sys.path.append("..")
from utils.Exceptions import handleSigterm,SigTermException

signal.signal(signal.SIGTERM,handleSigterm)

# Function that handles a connection
def connectionHandler(message,address):
    print(f"received from {address[0]}:{address[1]}:",message.decode("utf-8"))
    # Capitalize the message from the client
    message = message.upper()
    # Otherwise, the server response
    print(f"sent to {address[0]}:{address[1]}:",message.decode("utf-8"))
    serverSocket.sendto(message, address)

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 11000))
print("Server bound to port 11000")
while True:
    try:
        if threading.active_count() < 16:
            # Receive the client packet along with the address it is coming from
            message, address = serverSocket.recvfrom(1024)
            # Creating thread useful for server doing longer tasks, multiple users, and larger payloads
            th = threading.Thread(target=connectionHandler,args=(message,address))
            th.start()
    except (KeyboardInterrupt, SigTermException) as e:
        if type(e)==KeyboardInterrupt:
            print(f"Received either SIGINT")
        else:
            print(f"Received either SIGTERM")
        break
print("Closing server socket")
serverSocket.close()