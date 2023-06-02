import socket
import json
import sys

PORT=3389
IP='34.172.166.240'

def jsonSetUp(instruction:str, message):
    """
    :param instruction: It could NAN, TOOLCHG, MOVE, PHOTO, TURN_OFF
    :param message: any type of data to transmit
    :return: json file with configured parameters
    """

    # dictonary to create json file
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

def communicationClient(socketUser, instructions="NAN", message="NAN"):
    """
    :param socketUser:
    :param instructions: It can be NAN, TOOLCHG, MOVE, PHOTO, TURN_OFF
    :param message: any type of data sent
    :return: none or 3D pints list in case of PHOTO
    """
    # Json file creation
    json_data = jsonSetUp(instructions, message)

    if instructions == "MOVE" or instructions == "TOOLCHG" or instructions == "TURN_OFF":
        # Sending json file through a Socket
        print("Json data: ", json_data)
        socketUser.send(json_data.encode())  # Codificar para convertir los datos a binario

    elif instructions == "PHOTO":
        # Enviar datos a través de la conexión TCP del socket
        socketUser.send(json_data.encode())  # Codificar para convertir los datos a binario

        # How much data it gets from the socket
        buffer_size = 1024

        received_data = b""  # Data it is going to be received as bytes

        while True:
            # Receive data from socket connection
            data = socketUser.recv(buffer_size)

            if not data:
                break
            # Data concatenation
            received_data += data

        # Getting data from binary
        received_data = received_data.decode()

        print("Server data:", received_data)

        try:
            # Json string decode
            jsonData = json.loads(received_data)

            print("jsonData['message']:", jsonData["message"])

            return jsonData["message"] #returning 3D points of the face, there are inside "message" in json file

        except json.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))
            return None

    return None


if __name__ == '__main__':
    #In case you want to test some new feature, use this main function
    pass


