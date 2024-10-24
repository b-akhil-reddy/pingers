import select
from time import time
import struct

# Latest list of ICMP error messages are collected from RFC 792 and 
# https://datatracker.ietf.org/doc/html/rfc792
# https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
# Considered only the error messages in the above
# Function to identify the ICMP error
# Type 3 - Code 0 - Net Unreachable
# Type 3 - Code 1 - Host Unreachable
# Type 3 - Code 2 - Protocol Unreachable
# Type 3 - Code 3 - Port Unreachable
# Type 3 - Code 4 - Fragmentation Needed and Don't Fragment was Set
# Type 3 - Code 5 - Source Route Failed
# Type 3 - Code 6 - Destination Network Unknown
# Type 3 - Code 7 - Destination Host Unknown
# Type 3 - Code 8 - Source Host Isolated
# Type 3 - Code 9 - Communication with Destination Network is Administratively Prohibited
# Type 3 - Code 10 - Communication with Destination Host is Administratively Prohibited
# Type 3 - Code 11 - Destination Network Unreachable for Type of Service
# Type 3 - Code 12 - Destination Host Unreachable for Type of Service
# Type 3 - Code 13 - Communication Administratively Prohibited
# Type 3 - Code 14 - Host Precedence Violation
# Type 3 - Code 15 - Precedence cutoff in effect
# Type 4 - Code 0 - Source Quench
# Type 11 - Code 0 - Time to Live exceeded in Transit
# Type 11 - Code 1 - Fragment Reassembly Time Exceeded
# Type 12 - Code 0 - Pointer indicates the error
# Type 12 - Code 1 - Missing a Required Option
# Type 12 - Code 2 - Bad Length
# Type 40 - Code 0 - Bad SPI
# Type 40 - Code 1 - Authentication Failed
# Type 40 - Code 2 - Decompression Failed
# Type 40 - Code 3 - Decryption Failed
# Type 40 - Code 4 - Need Authentication
# Type 40 - Code 5 - Need Authorization
# Type 43 - Code 1 - Malformed Query
# Type 43 - Code 2 - No Such Interface
# Type 43 - Code 3 - No Such Table Entry
# Type 43 - Code 4 - Multiple Interfaces Satisfy Query
def icmpError(msgType,msgCode):
    if msgType == 3:
        if msgCode == 0:
            return "Net Unreachable"
        elif msgCode == 1:
            return "Host Unreachable"
        elif msgCode == 2:
            return "Protocol Unreachable"
        elif msgCode == 3:
            return "Port Unreachable"
        elif msgCode == 4:
            return "Fragmentation Needed and Don't Fragment was Set"
        elif msgCode == 5:
            return "Source Route Failed"
        elif msgCode == 6:
            return "Destination Network Unknown"
        elif msgCode == 7:
            return "Destination Host Unknown"
        elif msgCode == 8:
            return "Source Host Isolated"
        elif msgCode == 9:
            return "Communication with Destination Network is Administratively Prohibited"
        elif msgCode == 10:
            return "Communication with Destination Host is Administratively Prohibited"
        elif msgCode == 11:
            return "Destination Network Unreachable for Type of Service"
        elif msgCode == 12:
            return "Destination Host Unreachable for Type of Service"
        elif msgCode == 13:
            return "Communication Administratively Prohibited"
        elif msgCode == 14:
            return "Host Precedence Violation"
        elif msgCode == 15:
            return "Precedence cutoff in effect"
    elif msgType == 4:
        if msgCode == 0:
            return "Source Quench"
    elif msgType == 11:
        if msgCode == 0:
            return "Time to Live exceeded in Transit"
        elif msgCode == 1:
            return "Fragment Reassembly Time Exceeded"
    elif msgType == 12:
        if msgCode == 0:
            return "Pointer indicates the error"
        elif msgCode == 1:
            return "Missing a Required Option"
        elif msgCode == 2:
            return "Bad Length"
    elif msgType == 40:
        if msgCode == 0:
            return "Bad SPI"
        elif msgCode == 1:
            return "Authentication Failed"
        elif msgCode == 2:
            return "Decompression Failed"
        elif msgCode == 3:
            return "Decryption Failed"
        elif msgCode == 4:
            return "Need Authentication"
        elif msgCode == 5:
            return "Need Authorization"
    elif msgType==43:
        if msgCode == 1:
            return "Malformed Query"
        elif msgCode == 2:
            return "No Such Interface"
        elif msgCode == 3:
            return "No Such Table Entry"
        elif msgCode == 4:
            return "Multiple Interfaces Satisfy Query"

# Function to receive ICMP error messages
def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Request timed out"
        recPacket, addr = mySocket.recvfrom(1024)
        # Check if the ICMP packet is received from the destination
        if destAddr == addr[0]:
        # Fetch the ICMP header from the IP packet
            if recPacket != None:
                recvType,recvCode = struct.unpack_from("bb",recPacket,offset=20)
                # Check if response is an error
                err=icmpError(recvType,recvCode)
                if err:
                    return err
                return None
        
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out"