# importing required modules
from socket import *
from time import time,sleep
from datetime import datetime
import sys
import os
import signal

# Using PARTC of the assignment
sys.path.append("..")
# Importing utilities
from utils.ICMPErrors import receiveOnePing
from utils.Summary import summary
from utils.Exceptions import handleSigterm,SigTermException

# Handling SIGTERM
signal.signal(signal.SIGTERM,handleSigterm)

# defining a constant wait time of 1 second if no reply is received
wait = 1

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
# Variables to store number of sent and received packets
# This is incremented by 1 for every request
numSent = 0
# This is incremented by 1 for every request
numReceived = 0

# Variables storing the destination addresses
destAddr = '172.17.0.1'
destPort = 11001

# TCP socket to talk to the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket.settimeout(wait)
clientSocket.bind(('',32000))

# Connecting to the server
try:
    clientSocket.connect((destAddr,destPort))
except Exception as e:
    print(e)
    exit(e.strerror)
print(f"Connected to {destAddr}:{destPort}")

# Using the client socket and sending requests to the server
for i in range(N):
    # Sending request
    numSent+=1
    t1=time()
    msg=f"ping {i+1} {t1}"
    print(f"send to {destAddr}:{destPort}: {msg}")
    clientSocket.send(msg.encode("utf-8"))
    # Getting time at which request is sent
    try:
        # Waiting for response from the server and decoding it
        msg = clientSocket.recv(1024).decode("utf-8")
        # Getting time at which response is received
        t2 = time()
        numReceived+=1
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
    except (TimeoutError,KeyboardInterrupt,SigTermException,ConnectionError) as e:
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
print("Closing tcp socket")
clientSocket.close()
sleep(1)