import socket
from time import sleep

# Function that handles a connection
def connectionHandler(conn,clientaddr,clientport):
    while True:
        # Receive the data
        data = conn.recv(1024)
        # If there is no data then close connection so break out of while loop
        # If there is data then send a reply by converting received data to uppercase
        if data:
            print(f"received from {clientaddr}:{clientport}:",data.decode("utf-8"))
            inp = data.decode()
            try:
                conn.send(inp.upper().encode("utf-8"))
                print(f"sent to {clientaddr}:{clientport}",inp.upper())
            except:
                break
        else:
            print(f"received connection close request from {clientaddr}:{clientport}")
            break
    # Closing the connection
    conn.close()

if __name__ == "__main__":
    # Creating server socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("",11001))
    # Listening for connection
    print("Listening on port 11001")
    serverSocket.listen(1)

    # As this is not concurrent handle each connection one by one
    while True:
        try:
            # Handle only a single client at once
            conn, (clientaddr,clientport) = serverSocket.accept()
            print(f"Connected to {clientaddr}:{clientport}")
            connectionHandler(conn,clientaddr,clientport)
        except KeyboardInterrupt:
            print(f"Received either SIGINT")
            break
    # Closing server socket
    print("Closing server socket")
    serverSocket.close()