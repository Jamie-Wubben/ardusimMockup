import socket
import sys

if len(sys.argv) < 3:
    print("please give IP and port to talk to")
    exit()

ip = str(sys.argv[1])
port = int(sys.argv[2])

print("connecting with " + ip + " at port " + str(port))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("Do Ctrl+c to exit the program !!")

# Let's send data through UDP protocol
while True:
    send_data = input("Type some text to send =>");
    s.sendto(send_data.encode('utf-8'), (ip, port))
    print("\n\n 1. Client Sent : ", send_data, "\n\n")

s.close()