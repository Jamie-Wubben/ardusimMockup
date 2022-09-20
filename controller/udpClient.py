import socket
import sys
import json


def arm():
    msg = {"sender":"control",
            "command": "arm"}
    send_msg(json.dumps(msg))

def take_off():
    msg = {"sender":"control",
            "command": "take_off"}
    send_msg(json.dumps(msg))

def move(x,y,z):
    msg = {"sender":"control",
            "command": "move",
            "x":str(x),
            "y":str(y),
            "z":str(z)}
    send_msg(json.dumps(msg))

def land():
    msg = {"sender":"control",
            "command": "land"}
    send_msg(json.dumps(msg))

def send_msg(msg):
    ip = str(sys.argv[1])
    port = int(sys.argv[2])

    s.sendto(msg.encode('utf-8'), (ip, port))
    msgFromServer = s.recvfrom(1024)
    print(msgFromServer)
    


if len(sys.argv) < 3:
    print("please give IP and port to talk to")
    exit()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("Do Ctrl+c to exit the program !!")

# Let's send data through UDP protocol
while True:
    command = input("Choose command to send to UAV:\n\
    1: Arm\n\
    2: Take off\n\
    3: Move x 10m\n\
    4: Move y 10m\n\
    5: Land\n\
    =>")
    msg = ""
    match command:
        case "1":
            arm()
        case "2":
            take_off()
        case "3":
            move(10,0,0)
        case "4":
            move(0,10,0)
        case "5":
            land()

s.close()