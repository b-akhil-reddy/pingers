# importing required modules
from socket import *
from time import time
from datetime import datetime
import sys
import os
import signal
import struct
import select
from io import BytesIO

# Using PARTC of the assignment
sys.path.append("..")
# Importing utilities that are created
from utils.Summary import summary
from utils.ICMPErrors import receiveOnePing
from utils.Exceptions import SigTermException,handleSigterm
# defining a constant wait time of 1 second if no reply is received
wait = 1

# Set up the signal handler
signal.signal(signal.SIGTERM, handleSigterm)

# Checking if the user is root
try:
    # Socket to look for ICMP reply messages
    icmpProtocol = getprotobyname("icmp")
    icmpSocket = socket(AF_INET, SOCK_RAW, icmpProtocol)
    myID = os.getpid() & 0xFFFF
except PermissionError:
    print("This program must be run as a root user")
    exit(1)
print("ICMP socket opened to listen for ICMP messages")

# Taking number N as input from the user
N = input("Enter number of pings to be sent:\n")
while not N.isdecimal():
    print(f"Expected number as an input but received {N}")
    N = input("Enter number of pings to be sent:\n")
N = int(N)

# Maintaining variables to store the respective values
sumRTT = 0
maxRTT = 0
minRTT = float("inf")
# Variables to store number of packets sent and received packets
# This is incremented by 1 for every request
numSent = 0
# This is incremented by 1 for every response
numReceived = 0

# Variables storing the destination addresses
destAddr = '127.0.0.1'
destPort = 11000

# UDP Socket to talk to the server
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(wait)
# Using 31000 port instead of an ephemeral port
clientSocket.bind(('',31000))

# Using the client socket and sending requests to the server
for i in range(N):
    # Sending request
    numSent+=1
    # Getting initial time
    t1 = time()
    msg=f"ping {i+1} {t1}"
    print(f"send to {destAddr}:{destPort}: {msg}")
    clientSocket.sendto(msg.encode("utf-8"),(destAddr, destPort))
    try:
        # Waiting for response from the server
        msg, server = clientSocket.recvfrom(1024)
        # Getting time at which response is received
        t2 = time()
        # Decoding the message
        msg = msg.decode("utf-8")
        
        # Checking if the response is received from the server
        # If a response is received from another server it
        # should not be used for calculations.
        if server:
            if server[1] == 11000:
                # Calculating RTT in milli seconds and Rounding it to 3 decimal places
                rtt = round((t2-t1)*1000,3)
                # Logic for maximum
                if rtt>maxRTT:
                    maxRTT = rtt
                # Logic for minimum
                if rtt<minRTT:
                    minRTT = rtt
                # Adding rtt to sum for finding average
                sumRTT += rtt
                # Printing the message and RTT
                print(f"received from {destAddr}:{destPort}",msg,f"rtt={rtt:.3f}ms")
                numReceived+=1
            else:
                # Ignoring responses received on client socket from other servers
                print(f"Recevied data from address {server[0]}:{server[1]} while waiting for packet {i+1}")
    except (TimeoutError,KeyboardInterrupt,SigTermException) as e:
        if type(e) == TimeoutError:
            # If a timeout has occured checking if there is any corresponding ICMP message
            # Ignoring such case too for calculations
            try:
                err=receiveOnePing(icmpSocket,myID,wait,destAddr)
                if type(err)==str:
                    print(f"{err} for the packet {i+1}")
            except (KeyboardInterrupt,SigTermException) as e:
                if type(e) == KeyboardInterrupt:
                    print("Received interrupt stopping pings")
                else:
                    print("Received SIGTERM stopping pings")
                break
        else:
            # This interrupt is received before timeout is received
            # In this case the packet sent is not counted
            numSent-=1
            if type(e) == KeyboardInterrupt:
                print("Received interrupt stopping pings")
            else:
                print("Received SIGTERM stopping pings")
            break

# Calling the summary function
summary(numSent,numReceived,minRTT,maxRTT,sumRTT)

# Closing the sockets
print("Closing icmp socket")
icmpSocket.close()
print("Closing UDP socket")
clientSocket.close()