import socket
import json

PORT=3400
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

def communicationRobot(socketUser):
    """
     instruction: It could NAN, TOOLCHG, MOVE, PHOTO, TURN_OFF
    """
    #It's listening until recive data from server
    while True:
        serverData = socketUser.recv(1024)
        if serverData:
            print("DATA RECIBIDA")
            jsonData = json.loads(serverData.decode())
            instruction=jsonData["instruction"]
            print(jsonData)

            if instruction == "MOVE":
                #Sending coordenates to arduino
                pass

            elif instruction == "TOOLCHG":
                pass

            elif instruction == "PHOTO":
                #Getting images

                images="IMAGES"

                # data set to json
                json_data = jsonSetUp("NAN", images)
                print(json_data)

                # sending data through TCP socket connection
                socketUser.send(json_data.encode())  # encode transform data to binary

                pass

            elif instruction == "TURN_OFF":
                #robot turn off
                pass

if __name__ == '__main__':

    socketClient=connectionSocket(IP, PORT)

    communicationRobot(socketClient)

