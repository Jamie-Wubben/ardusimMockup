from abc import ABC, abstractmethod
import zmq
import threading
import time

addr_application = "tcp://*:10001"
addr_status = "tcp://*:10000"

class DroneControllerInterface(ABC):

    @abstractmethod
    def takeoff():
        pass

    @abstractmethod
    def move(x,y,z):
        pass
    
    @abstractmethod
    def land():
        pass

    def listenToNetwork():
        pass

    @abstractmethod
    def publishStatus():
        pass


class Copter(DroneControllerInterface):
    def __init__(self,numUAV):
        self.numUAV = numUAV
        self.x =0
        self.y =0
        self.z =0
        self.running = True

        self.context = zmq.Context()


        thread = threading.Thread(target=self.publishStatus)
        thread.start()

    def takeoff(self):
        self.z = self.z + 10

    def move(self,x,y,z):
        _x = float(x)
        _y = float(y)
        _z = float(z)
        self.x = self.x + _x
        self.y = self.y + _y
        self.z = self.z + _z

    def land(self):
        self.running = False
        self.z = 0

    def getStatus(self):
        return self.x, self.y, self.z

    def printStatus(self):
        print(self.x, self.y, self.z)

    def listenToNetwork(self):
        socket = self.context.socket(zmq.PAIR)
        socket.bind(addr_application)
        running = True
        while running:
            msg = (socket.recv()).decode("utf-8")
            command = msg.split()
            
            method_name = command[0]
            params = command[1:]
            method = getattr(c,method_name)
            method(*params)

            if msg == "land":
                running = False

    def publishStatus(self):
        socket = self.context.socket(zmq.PUB)
        socket.bind(addr_status)
        while self.running:
            data = {
                "source": "Drone/copter",
                "type":"internal",
                "data":{
                    "msg":"status",
                    "vehicle_type":"drone",
                    "id":self.numUAV,
                    "pos_x":self.x,
                    "pos_y":self.y,
                    "pos_z":self.z
                }
            }
            socket.send_json(data)
            time.sleep(1)

if __name__ == '__main__':
    c = Copter(1)
    c.listenToNetwork()


