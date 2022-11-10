import zmq
from math import sqrt

context = zmq.Context()
numUAV = "1"
socket_status_uav = context.socket(zmq.SUB)
socket_status_uav.connect("tcp://localhost:10000")
socket_status_uav.setsockopt_string(zmq.SUBSCRIBE, "Status_UAV")

socket_algo = context.socket(zmq.PUSH)
socket_algo.connect("tcp://localhost:10003")

minimal_distance = 5
location_UAVs = {}
location_UAVs["0"] = [50,50,10]

def update_location(data):
	numUAV = data[1]
	x = float(data[2])
	y = float(data[3])
	z = float(data[4])
	loc = [x,y,z]
	location_UAVs[numUAV] = loc

def calculate_distance(loc1, loc2):
	dx = loc1[0] - loc2[0]
	dy = loc1[1] - loc2[1]
	dz = loc1[2] - loc2[2]

	distance = sqrt(dx*dx + dy*dy + dz*dz)
	return distance


running = True
counter = 0
while running:
	msg = socket_status_uav.recv_string()
	data = msg.split()
	if len(data) == 5:
		update_location(data)
	
	if numUAV in location_UAVs.keys():
		#basemessage
		msg = {
			"source": "algo/collision_avoidance",
			"msg_type": "internal"
		}

		for num_uav,loc in location_UAVs.items():
			if numUAV != num_uav:
				d = calculate_distance(location_UAVs[numUAV],loc)
				if d < minimal_distance and counter < 10:
					msg["data"] = {"collision_thread": True, "colliding_with_UAV":num_uav}
					counter = counter+1
				else:
					msg["data"] = {"collision_thread": False}

				print(msg["data"])
				socket_algo.send_json(msg)

