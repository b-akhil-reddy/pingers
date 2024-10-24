# About
This repository contains implementations of ping servers and clients for UDP, and TCP protocol and a client for ICMP protocols. These implementations allow testing network connectivity and round trip time. Each implementation showcases unique features and handling mechanisms for the respective protocols, making it a versatile toolkit. The UDP and TCP implementations also include ICMP error message handling such that on receiving an ICMP error message from the ping server the respective error messages are printed on the console. It also provides statistics on the round trip time to understand the stability of the connection.

# Directory Structure
The [utils](./utils/) package was written to maintain all the utility functionality at a single place. The file [ICMPErrors.py](./utils/ICMPErrors.py) has functions to identify the ICMP error message based on the ICMP message headers and also code to handle ICMP messages from a server. The file [Summary.py](./utils/Summary.py) has a function to print the summary. Other than the utils directory the main directory [/](.) contains three folders UDPPinger, TCPPinger, ICMPPinger. UDPPinger folder contains files related to UDP Servers and Client as required. TCPPinger folder contains files related to TCP Servers and Client as required. ICMPPinger folder contains files related to ICMP client as required. This directory strucutre was followed to provide modularity. Following is the tree diagram for the same:
<pre>
.
├── <a href="./UDPPinger">UDPPinger</a>
│   ├── <a href="./UDPPinger/UDPPingerClient.py">UDPPingerClient.py</a>
│   ├── <a href="./UDPPinger/UDPPingerModifiedServer.py">UDPPingerModifiedServer.py</a>
│   └── <a href="./UDPPinger/UDPPingerServer.py">UDPPingerServer.py</a>
├── <a href="./TCPPinger/">TCPPinger</a>
│   ├── <a href="./TCPPinger/TCPPingerClient.py">TCPPingerClient.py</a>
│   ├── <a href="./TCPPinger/TCPPingerModifiedServer.py">TCPPingerModifiedServer.py</a>
│   └── <a href="./TCPPinger/TCPPingerServer.py">TCPPingerServer.py</a>
├── <a href="./ICMPPinger">ICMPPinger</a>
│   └── <a href="./ICMPPinger/ICMPPingerClient.py">ICMPPingerClient.py</a>
├── <a href="./utils">utils</a>
|   ├── <a href="./utils/ICMPErrors.py">ICMPErrors.py</a>
|   └── <a href="./utils/Summary.py">Summary.py</a>
└── README.md
</pre>

# Running the Programs
To execute the client programs change the present working directory to the directory where the client program is present. To change the directory use the following command:
```
cd <directory-name>
```
Replace `<directory-name>` with appropriate directory name. `<directory-name>` can be one of `UDPPinger`, `TCPPinger` or `ICMPPinger`

All the clients should have privileges to run the program. The reason for this is to allow the parsing of ICMP messages with the help of raw sockets. Following is the command to run the respective client programs.
```bash
sudo python3 <client-program-file>
```
Replace `<client-program-file>` with appropriate filename.

Following command can be used to run the server program it doesn't need to have any privileges.
```bash
python3 <server-program-file>
```
Replace `<server-program-file>` with appropriate filename.


```
Note: Every program expects an input number N from the keyboard through a prompt giving. Program would prompt again for incorrect input values.
```

# Brief Descriptions of Programs
- <a href="./UDPPinger/UDPPingerServer.py">UDPPingerServer.py</a><br>This program contains the code for a simple UDP server which on receiving a message on `11000` port capitalizes the text and sends back the text to the client. It also simulates packet loss with the help of `randint` function.
- <a href="./UDPPinger/UDPPingerClient.py">UDPPingerClient.py</a><br>This is the client program that takes positive integer `N` as an input and tries sending `N` probes to the server. It also provides summary of Round Trip Time per each request and at the end it provides the metrics MIN RTT, MAX RTT, AVG RTT, Number of Packets Sent, Number of Packets Received, and Percentage of Packets lost. This program handles `SIGINT` and `SIGTERM` signals. On sending one of these signals program gracefully shutdowns closing all the sockets  and provides summary of the results acquired so far. It also opens an ICMP socket to receive ICMP messages from the server after `recvfrom` raises a timeout.
- <a href="./UDPPinger/UDPPingerModifiedServer.py">UDPPingerModifiedServer.py</a><br>This program is a slightly modified version of the basic UDP server. Instead of simulating the packet loss in the application level this program expects packets are lost. To simulate the packet loss in this case `tc` traffic controller command is used before starting this server. Alongside this it also makes use of multithreading to improve performance. Also this implementation takes care about exception that can occur on the server.
- <a href="./TCPPinger/TCPPingerServer.py">TCPPingerServer.py</a><br>This program contains the code for a simple TCP server which on receiving a message on `11001` port capitalizes the text and sends it back to the client. And it is a single threaded program because of which a the server can handle only a single client at any point in time.
- <a href="./TCPPinger/TCPPingerClient.py">TCPPingerClient.py</a><br>This is the client program that takes positive integer `N` as an input and tries sending `N` probes to the server. It also provides summary of Round Trip Time per each request and at the end it provides the metrics MIN RTT, MAX RTT, AVG RTT, Number of Packets Sent, Number of Packets Received, and Percentage Packets lost. This program handles `SIGINT` and `SIGTERM` signals. On sending one of these signals program gracefully shutdowns closing all the sockets  and provides summary of the results acquired so far. It also opens an ICMP socket to receive ICMP messages from the server if `recv` raises a timeout.
- <a href="./TCPPinger/TCPPingerModifiedServer.py">TCPPingerModifiedServer.py</a><br>This program is a slightly modified version of the basic TCP server. In this case multiple threads are used to handle multiple clients. Also this implementation takes care about exception that can occur on the server.
- <a href="./ICMPPinger/ICMPPingerClient.py">ICMPPingerServer.py</a><br>This is the client program that takes positive integer `N` as an input and tries sending `N` probes to the server. It also provides summary of Round Trip Time per each request and at the end it provides the metrics MIN RTT, MAX RTT, AVG RTT, Number of Packets Sent, Number of Packets Received, and Percentage Packets lost. This program handles `SIGINT` and `SIGTERM` signals. On sending one of these signals program gracefully shutdowns closing all the sockets  and provides summary of the results acquired so far. It also parses the ICMP error messages and prints it accordingly on the console.

<pre>
Note that all our findings have been reported in <a href="./Report.pdf">Report.pdf</a> file.
</pre>