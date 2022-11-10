import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:10000")
socket.setsockopt(zmq.SUBSCRIBE, b'')


while True:
	msg = socket.recv_json()

	if msg["source"] == "Drone/copter":
		data = msg["data"]
		print(data["id"], ": ", data["pos_x"], " ", data["pos_y"], " ", data["pos_z"])