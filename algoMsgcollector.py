import zmq
import json

context = zmq.Context()
socket_algorithms = context.socket(zmq.PULL)
socket_algorithms.bind("tcp://*:10003")

socket_publish = context.socket(zmq.PUB)
socket_publish.bind("tcp://*:10002")

def check_valid(msg):
	return {"source","msg_type","data"}.issubset(msg)


def handle_multi_uav_msg():
	pass

def handle_master_slave_msg():
	pass


running = True
while running:
	msg = socket_algorithms.recv_json()

	if not check_valid(msg):
		print("error this message is not valid")
		print(msg)

	msg_type = msg["msg_type"] 

	match msg_type:
		case "internal":
			socket_publish.send_string("algoCollector " + json.dumps(msg))
		case "multi_uav":
			handle_multi_uav_msg()
		case "master_slave":
			handle_master_slave_msg()
		case _:
			print("error type not recognized")
