import socket
import json
import select
import time

PORT_USER = 3389
PORT_ROBOT = 3400

# User's socket creation
sockListenUser = socket.socket()
print("USER Socket successfully created")
sockListenUser.bind(('', PORT_USER))
print("socket binded to %s" % (PORT_USER))

# Robot's socket creation
sockListenRobot = socket.socket()
print("ROBOT Socket successfully created")
sockListenRobot.bind(('', PORT_ROBOT))
print("socket binded to %s" % (PORT_ROBOT))

sockListenUser.listen(5)
print("socket USER is listening")
socketConnListenUser, addr = sockListenUser.accept()
socketConnListenUser.setblocking(0)
print('Got connection from', addr)

sockListenRobot.listen(5)
print("socket ROBOT is listening")
socketConnListenRobot, addr2 = sockListenRobot.accept()
socketConnListenRobot.setblocking(0)
print('Got connection from', addr2)

while True:
    # use select to wait for data to be available on the socket
    ready_to_read, _, _ = select.select([socketConnListenUser, socketConnListenRobot], [], [], 0.1)

    # if data is available, receive it from the socket
    for socketConn in ready_to_read:
        try:
            data = socketConn.recv(1024)
            if socketConn == socketConnListenUser:
                # If there is data from robot, it will be sent to ROBOT
                if data:
                    socketConnListenUser.send(data)
            elif socketConn == socketConnListenRobot:
                #If there is data from robot, it will be sent to USER
                if data:
                    #HERE CALL TO CLOUD FUNCIONS
                    #json=json.loads(data.decode())
                    #images=json["message"]
                    #points3d=CLOUDFUNCTION
                    #json["message"]=points3d
                    #data=json.dumps(data).encode()
                    socketConnListenUser.send(data)

        except BlockingIOError:
            pass
    else:
        #Delay to verify if there is new data in some socket
        time.sleep(0.1)