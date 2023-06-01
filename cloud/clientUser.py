import socket
import json


PORT=3389
IP='34.172.166.240'

def jsonSetUp(instruction:str, message):
    """
    :param instruction: It could NAN, TOOLCHG, MOVE, PHOTO
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


def connectionSocket(ip, port:int):
    """"
    Socket creation and connection
    """
    s = socket.socket()  # socket creation
    s.connect((ip, port))
    return s

def communicationClient(socketUser, instruccions="NAN", message="NAN"):
    """
    :param socketUser:
    :param instruccions: It could NAN, TOOLCHG, MOVE, PHOTO, TURN_OFF
    :param message: any type of data to be sent
    :return:
    """
    # data set to json
    json_data = jsonSetUp(instruccions, message)


    if instruccions == "MOVE" or instruccions == "TOOLCHG":
        # sending data through TCP socket connection
        socketUser.send(json_data.encode())  # encode transform data to binary

    elif instruccions == "PHOTO":
        # sending data through TCP socket connection
        socketUser.send(json_data.encode())  # encode transform data to binary

        #Socket block until recive data
        serverData = socketUser.recv(1024).decode()
        jsonData = json.loads(serverData)
        print(jsonData["message"])

        #return



if __name__ == '__main__':

    socketClient=connectionSocket(IP, PORT)

    communicationClient(socketClient, instruccions="PHOTO")

