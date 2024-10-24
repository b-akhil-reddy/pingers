# We will need the following module to generate randomized lost packets
import random
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 11000))
print("Server bound to port 11000")
while True:
    # Generate a random number between 1 to 10 (both inclusive)
    rand = random.randint(1, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    print(f"received from {address[0]}:{address[1]}:",message.decode("utf-8"))
    # Capitalize the message from the client
    message = message.upper()
    # If rand is greater than 8, we consider the packet lost and do not respond to the client
    if rand > 8:
        print(f"dropped message: {message.decode()}")
        continue
    # Otherwise, the server response
    print(f"sent to {address[0]}:{address[1]}:",message.decode("utf-8"))
    serverSocket.sendto(message, address)