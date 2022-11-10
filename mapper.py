import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect ("tcp://localhost:10000")

socket.setsockopt_string(zmq.SUBSCRIBE, "Status_UAV")

while True:
	msg = socket.recv_string()
	print(msg)