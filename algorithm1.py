import zmq

context = zmq.Context()
socket_status_uav = context.socket(zmq.SUB)
socket_status_uav.connect("tcp://localhost:10000")
socket_status_uav.setsockopt(zmq.SUBSCRIBE, b'')

socket_algo = context.socket(zmq.PUSH)
socket_algo.connect("tcp://localhost:10003")

final_position_x = 100
final_position_y = 100
final_position_z = 10

running = True
while running:
	msg = socket_status_uav.recv_json()
	data = msg["data"]
	
	if data["msg"] == "status":
		x = data["pos_x"]
		y = data["pos_y"]
		z = data["pos_z"]

		dx = final_position_x - x
		dy = final_position_y - y
		dz = final_position_z - z

		if abs(dx) < 3 and abs(dy) < 3 and abs(dz) < 3:
			msg = {
				"source": "algo/mission",
				"msg_type": "internal",
				"data": {
					"action": "land"
				}
			}
			running = False
		else:
			msg = {
				"source": "algo/mission",
				"msg_type": "internal",
				"data": {
					"action": "move",
					"x": dx,
					"y": dy,
					"z": dz
				}
			}
		socket_algo.send_json(msg)
