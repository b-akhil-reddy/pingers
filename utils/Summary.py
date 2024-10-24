# Function to print the summary
def summary(numSent,numReceived,minRTT,maxRTT,sumRTT):
    # Properly formatting the text
    lines="="*20
    print(lines)
    # Summarizing the results
    print("Summary:")
    print(lines)
    # Handling zero division error
    if numSent==0:
        print("No packets are sent")
        print(f"Packets Sent: {numSent}")
        print(f"Packets Received: {numReceived}")
        print(f"MIN RTT: NA")
        print(f"MAX RTT: NA")
        print(f"AVG RTT: NA")
        print(f"Loss Rate: NA")
    elif numReceived==0:
        # Printing an extra statement saying no response
        print("No response received from server")
        print(f"Packets Sent: {numSent}")
        print(f"Packets Received: {numReceived}")
        print(f"MIN RTT: NA")
        print(f"MAX RTT: NA")
        print(f"AVG RTT: NA")
        print(f"Loss Rate: {(1-numReceived/numSent)*100:.3f}%")
    else:
        print(f"Packets Sent: {numSent}")
        print(f"Packets Received: {numReceived}")
        print(f"MIN RTT: {minRTT:.3f}ms")
        print(f"MAX RTT: {maxRTT:.3f}ms")
        avgRTT = round(sumRTT/numReceived,3)
        print(f"AVG RTT: {avgRTT:.3f}ms")
        print(f"Loss Rate: {(1-numReceived/numSent)*100:.3f}%")
    print(lines)