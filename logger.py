from datetime import datetime
import zmq
import json

context = zmq.Context()
socket_status_uav = context.socket(zmq.SUB)
socket_status_uav.connect("tcp://localhost:10000")
socket_status_uav.setsockopt(zmq.SUBSCRIBE, b'')

now = datetime.now()
filename = now.strftime("log_%Y_%d_%m_%H_%M_%S.txt")

while True:
	msg = socket_status_uav.recv_string()
	with open(filename,"a") as file:
		file.write(msg + "\n")
