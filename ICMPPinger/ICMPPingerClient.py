from socket import *
import os
import sys
import struct
import time
import select
import signal
sys.path.append("..")
from utils.ICMPErrors import icmpError
from utils.Summary import summary

# Custom exception for handling SIGTERM
class SigTermException(Exception):
    pass

# Signal handler function
def handleSigterm(signum, frame):
    raise SigTermException("SIGTERM received")

# Set up the signal handler
signal.signal(signal.SIGTERM, handleSigterm)

ICMP_ECHO_REQUEST = 8

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Request timed out"

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        # Fill in start
        # Check if the ICMP packet is received from the destination
        if destAddr == addr[0]:
            # Fetch the ICMP header from the IP packet
            if recPacket != None:
                # Unpack the response to get TTL
                ttl = struct.unpack_from("b",recPacket,offset=8)
                # Unpacking the response to get ICMP headers
                recvType,recvCode,recvChecksum,id,seqno,timestamp = struct.unpack_from("bbHHhd",recPacket,offset=20)
                # Calculating Checksum
                calcChecksum=ntohs(checksum(struct.pack("bbHHhd",recvType,recvCode,0,id,seqno,timestamp)))
                # Verifying checksum id and sequence number
                if calcChecksum==recvChecksum and id==ID and seqno==1:
                    rtt = (timeReceived-timestamp)*1000
                    print(f"{len(recPacket)} bytes from {destAddr}: ttl={ttl[0]} rtt={rtt:.3f}ms")
                    return rtt
                # Check if response is an error
                err=icmpError(recvType,recvCode)
                if err:
                    return err
        # Fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out"

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0

    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put it in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects which can be referenced by their   
    # position number within the object.


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details: 
    # http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process ID
    try:
        sendOnePing(mySocket, destAddr, myID)
    except os.error as e:
        exit(e.strerror)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    try:
        dest = gethostbyname(host)
    except gaierror as e:
        print(e.strerror)
        exit(e.errno)
    print("Pinging " + dest + " using Python:")
    print("")

    # taking number N as input from the user
    N = input("Enter number of pings to be sent:\n")
    while not N.isdecimal():
        print(f"Expected number as an input but received {N}")
        N = input("Enter number of pings to be sent:\n")

    N = int(N)

    # Variables to store RTT metrics
    sumRTT = 0
    maxRTT = 0
    minRTT = float("inf")
    # Variables to count the number of sent and received packets
    numSent = 0
    numReceived = 0
    # Trying out pings N times
    for i in range(N):
        try:
            # Incrementing numSent and sending a request
            numSent+=1
            # Only if RTT is a number response is received otherwise an error is returned
            rtt = doOnePing(dest,timeout)
            # checking if rtt is string
            if type(rtt) == str:
                print(f"{rtt} for packet {i+1}",rtt)
                continue
            else:
                if rtt>maxRTT:
                    maxRTT = rtt
                if rtt<minRTT:
                    minRTT = rtt
                sumRTT += rtt
                numReceived+=1
        except PermissionError:
            print("This program must be run as a root user")
            exit(1)
        except (KeyboardInterrupt,SigTermException) as e:
            if type(e)==KeyboardInterrupt:
                print(f"Received either SIGINT")
            else:
                print(f"Received either SIGTERM")
            break
    summary(numSent,numReceived,minRTT,maxRTT,sumRTT)

if __name__ == "__main__":
    ping("localhost")