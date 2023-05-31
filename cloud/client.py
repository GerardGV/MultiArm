import socket
import json
import sys


def jsonSetUp(instruction:str, message):
    """
    :param instruction: It could NAN, TOOLCHG, MOVE
    :param message: any type of data to transmit
    :return: json file with configured parameters
    """

    #dictonary to create json file
    data = {
        "instruction": instruction,
        "message": message
    }

    # dictionary becomes json file
    json_data = json.dumps(data)

    return json_data

def sentDataServer(json_data, ip:str, port:int):

    socket.send(json_data.encode())
    s = socket.socket()
    s.connect((ip, port))
    print(s.recv(1024).decode())
    s.close()

if __name__ == '__main__':
    """
    Every time it's needed to sent data a scoket will be created.
    sys.argv[0] is not taken because it's the script name
    sys.argv[1] instruction robot
    sys.argv[2] data to transmit
    sys.argv[3] IP destination string
    sys.argv[4] port detination integrer
    """

    #data set to json
    json = jsonSetUp(sys.argv[1], sys.argv[2])

    #sending data trhough TCP socket connection
    sentDataServer(json, sys.argv[3], sys.argv[4])