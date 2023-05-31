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

def communication(sent:bool, socketUser, instruccions="Nan", message="Nan"):

    #It's going to be listening or It's gointo to sent a message
    if sent == True:
        # data set to json
        json_data = jsonSetUp(instruccions, message)

        # sending data through TCP socket connection
        socketUser.send(json_data.encode())  # encode transform data to binary

    else:
        #It's listening until recive data from server
        while True:
            serverData = socketUser.recv(1024).decode()
            if serverData:
                print("Data from SERVER")
                jsonData = json.loads(serverData)
                print(jsonData["message"])
                break

if __name__ == '__main__':

    socketClient=connectionSocket(IP, PORT)

    communication(False, socketClient)

