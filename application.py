import zmq
import json
from math import sqrt

addr_copter = "tcp://localhost:10001"
addr_algo = "tcp://localhost:10002"

collision_thread = True


def mag(vector):
    som = 0
    for element in vector:
        som = som + (element*element)

    return sqrt(som)

def normalize(vector):
    normalized = []
    magnitude = mag(vector)
    for element in vector:
        normalized.append(element/magnitude)
    return normalized


def input_from_user():
    command = input("send command to UAV: ")
    socket_copter.send_string(command)
    if command == "land":
        running = False

def perform_mission_action(msg):
    if not collision_thread:
        action = msg["action"]
        if action == "land":
            socket_copter.send_string("land")
        elif action == "move":
            missing_displacement = [msg["x"], msg["y"], msg["z"]]
            direction = normalize(missing_displacement)
            speed = 5
            command = "move " + str(round(direction[0]*speed)) + " " + str(round(direction[1]*speed)) + " " + str(round(direction[2]*speed))
            socket_copter.send_string(command)
            print(command)
    else:
        print("collision_thread I won't move")

def perform_collision_avoidance_action(msg):
    global collision_thread
    collision_thread = msg["collision_thread"]


def handle_msg(msg):
    source = msg["source"]
    if source == "algo/mission":
        perform_mission_action(msg["data"])
    elif source == "algo/collision_avoidance":
        perform_collision_avoidance_action(msg["data"])



if __name__ == '__main__':

    context = zmq.Context()
    socket_copter = context.socket(zmq.PAIR)
    socket_copter.connect(addr_copter)

    socket_algo = context.socket(zmq.SUB)
    socket_algo.connect(addr_algo)
    socket_algo.setsockopt(zmq.SUBSCRIBE, b'')

    socket_copter.send_string("takeoff")
    running = True
    while running:
        try:
            msg = socket_algo.recv_string(flags=zmq.NOBLOCK)
            msg_json = json.loads(msg.split(maxsplit=1)[1])
            
            handle_msg(msg_json)
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                pass # no message
            else:
                print(e)